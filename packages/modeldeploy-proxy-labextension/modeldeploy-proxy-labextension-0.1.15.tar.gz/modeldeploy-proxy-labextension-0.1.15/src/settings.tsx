import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { JSONObject } from '@lumino/coreutils';
import { Kernel } from '@jupyterlab/services';
import NotebookUtils from './lib/NotebookUtils';
import { executeRpc } from './lib/RPCUtils';

export const SETTINGS_ID = 'modeldeploy-proxy-labextension:settings';
const TRFANFORMER_CONFIG = 'transformerConfig';

let transformerEnabled: boolean = false;
let transformerNotebookDir: string = "";
let transformerProxyUrl: string = "";

export const getTransformerEnabled = (): boolean => {
    return transformerEnabled;
};

export const setTransformerEnabled = (settings: ISettingRegistry.ISettings, enabled: boolean) => {
    transformerEnabled = enabled;
    let config : IConfig = {
        enabled: enabled,
        notebookDir: transformerNotebookDir,
        proxyUrl: transformerProxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

export const getTransformerNotebookDir = (): string => {
    return transformerNotebookDir;
};

export const setTransformerNotebookDir = (settings: ISettingRegistry.ISettings, notebookDir: string) => {
    transformerNotebookDir = notebookDir;
    let config : IConfig = {
        enabled: transformerEnabled,
        notebookDir: notebookDir,
        proxyUrl: transformerProxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

export const getTransformerProxyUrl = (): string => {
    return transformerProxyUrl;
};

export const setTransformerProxyUrl = (settings: ISettingRegistry.ISettings, proxyUrl: string) => {
    transformerProxyUrl = proxyUrl;
    let config : IConfig = {
        enabled: transformerEnabled,
        notebookDir: transformerNotebookDir,
        proxyUrl: proxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

interface IConfig {
    enabled: boolean;
    notebookDir: string;
    proxyUrl: string;
}

const defaultConfig: IConfig = {
    enabled: false,
    notebookDir: "",
    proxyUrl: ""
}

export default {
    id: SETTINGS_ID,
    requires: [ ISettingRegistry ],
    autoStart: true,
    activate: (
        app: JupyterFrontEnd,
        settingRegistry: ISettingRegistry
    ): void => {
        Promise.all([settingRegistry.load(SETTINGS_ID)]).then(async ([settings]) => {
            try {
                let transformerSettings = settings.get(TRFANFORMER_CONFIG).composite as JSONObject;
                if(typeof transformerSettings.enabled === 'string') {
                    if(transformerSettings.enabled === 'true') {
                        transformerEnabled = true;
                    } else {
                        transformerEnabled = false;
                    }
                } else if(typeof transformerSettings.enabled === 'boolean') {
                    transformerEnabled = transformerSettings.enabled
                }

                if(typeof transformerSettings.notebookDir === 'string') {
                    transformerNotebookDir = transformerSettings.notebookDir;
                }

                if(typeof transformerSettings.proxyUrl === 'string') {
                    transformerProxyUrl = transformerSettings.proxyUrl;
                } else if(typeof transformerSettings.proxyUrl === 'number') {
                    transformerProxyUrl = transformerSettings.proxyUrl.toString();
                }
            } catch (error) {
                settingRegistry.set(SETTINGS_ID, TRFANFORMER_CONFIG, defaultConfig as unknown as JSONObject).catch((reason: Error) => {
                    console.error('Failed to set transformer config: ' + reason.message);
                });
            }
            try {
                const kernel: Kernel.IKernelConnection = await NotebookUtils.createNewKernel();
                const proxy_info = await executeRpc(kernel, 'proxy.info');
                kernel.shutdown();
                if(proxy_info.directory && proxy_info.directory !== transformerNotebookDir) {
                    console.log("Change notebook directory to: " + proxy_info.directory);
                    setTransformerNotebookDir(settings, proxy_info.directory);
                }
                if(proxy_info.proxy_url && proxy_info.proxy_url !== transformerProxyUrl) {
                    console.log("Change proxy URL to: " + proxy_info.proxy_url);
                    setTransformerProxyUrl(settings, proxy_info.proxy_url);
                }
                console.log("Proxy status: " + proxy_info.proxy_status);
            } catch (e) {
                console.warn("Unable to get settings form kernel!");
                console.warn(e);
            }
            console.log("Settings when starts up: enabled(" + transformerEnabled + "), NotebookDir(" + transformerNotebookDir + "), ProxyUrl(" + transformerProxyUrl + ")");
        });
    },
} as JupyterFrontEndPlugin<void>;
