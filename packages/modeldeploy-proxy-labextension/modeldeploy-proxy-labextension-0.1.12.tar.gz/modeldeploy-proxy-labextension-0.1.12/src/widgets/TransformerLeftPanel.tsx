import * as React from 'react';
import { ThemeProvider } from '@material-ui/core/styles';
import { theme } from './../theme';
import { executeRpc, globalUnhandledRejection } from './../lib/RPCUtils';
import NotebookUtils from './../lib/NotebookUtils';
import { Kernel } from '@jupyterlab/services';
import { Switch } from '@material-ui/core';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { getTransformerEnabled, setTransformerEnabled, getTransformerProxyUrl } from './../settings';
import { getTransformerNotebookDirectory } from './../notebook';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle } from '@material-ui/core';

interface IProps {
    transformerSettings: ISettingRegistry.ISettings
}

type ClickHandler = () => void;
interface IState {
    isEnabled: boolean;
    dialogTitle: string;
    dialogContent: string;
    isDialogVisible: boolean;
    isDialogCloseButtonVisible: boolean;
    closeButtonText: string;
    isDialogConfirmButtonVisible: boolean;
    dialogConfirmClickHandler: ClickHandler;
}

interface IDialogParams {
    visible?: boolean;
    title?: string;
    content?: string;
    isCloseButtonVisible?: boolean;
    closeButtonText?: string;
    isConfirmButtonVisible?: boolean;
}

export class TransformerLeftPanel extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);
        this.onDialogCloseClick = this.onDialogCloseClick.bind(this);
        this.onDialogConfirmClick = this.onDialogConfirmClick.bind(this);
        this.doResetTransformer = this.doResetTransformer.bind(this);
        this.doReloadPage = this.doReloadPage.bind(this);
        const defaultState: IState = {
            isEnabled: getTransformerEnabled(),
            isDialogVisible: false,
            isDialogCloseButtonVisible: true,
            dialogTitle: '',
            dialogContent: '',
            closeButtonText: 'Ok',
            isDialogConfirmButtonVisible: false,
            dialogConfirmClickHandler: this.onDialogConfirmClick
        };
        this.state = defaultState;
    }

    renderDialog({
        visible,
        title,
        content,
        isCloseButtonVisible,
        closeButtonText,
        isConfirmButtonVisible
    }: IDialogParams) {
        this.setState({
            isDialogVisible: visible !== undefined? visible: true,
            dialogTitle: title !== undefined? title: '',
            dialogContent: content !== undefined? content: '',
            isDialogCloseButtonVisible: isCloseButtonVisible !== undefined? isCloseButtonVisible: true,
            closeButtonText: closeButtonText !== undefined? closeButtonText: 'Ok',
            isDialogConfirmButtonVisible: isConfirmButtonVisible !== undefined? isConfirmButtonVisible: false
        });
    }

    onDialogCloseClick() {
        this.renderDialog({
            visible: !this.state.isDialogVisible
        });
    }

    onDialogConfirmClick() {
        console.log("onDialogConfirmClick");
        this.renderDialog({
            visible: !this.state.isDialogVisible
        });
    }

    componentDidMount = () => {
    };

    componentDidUpdate = (
        prevProps: Readonly<IProps>,
        prevState: Readonly<IState>,
    ) => {
    };

    applyTransformerToProxy = async () => {
        console.log('applyTransformerToProxy');
        this.renderDialog({
            title: 'Running',
            content: 'It will take few seconds!',
            isCloseButtonVisible: false
        });

        let proxyUrl: string = getTransformerProxyUrl();
        if(! proxyUrl) {
            this.renderDialog({
                title: 'Error',
                content: 'Unable to get the proxy URL!'
            });
            return;
        }

        try {
            const kernel: Kernel.IKernelConnection = await NotebookUtils.createNewKernel();
            const args = {
                proxy_url: proxyUrl,
                source_notebook_path: getTransformerNotebookDirectory()
            }
            await executeRpc(kernel, 'proxy.apply', args);
            kernel.shutdown();
            this.renderDialog({
                title: 'Done',
                content: 'The transforming is completed!!'
            });
        } catch (error) {
            globalUnhandledRejection({ reason: error });
            this.renderDialog({
                title: 'Error',
                content: error
            });
            throw error;
        }
    };

    resetTransformer = () => {
        console.log('resetTransformer');
        this.renderDialog({
            title: 'Warning',
            content: 'It will reset transformer.ipynb and you may lose your customized content!',
            closeButtonText: 'Cancel',
            isConfirmButtonVisible: true
        });
        this.setState({ dialogConfirmClickHandler: this.doResetTransformer });
    };

    doResetTransformer = async () => {
        console.log("doResetTransformer");
        let proxyUrl: string = getTransformerProxyUrl();
        if(! proxyUrl) {
            this.renderDialog({
                title: 'Error',
                content: 'Unable to get the proxy URL!'
            });
            this.setState({ dialogConfirmClickHandler: this.onDialogConfirmClick });
            return;
        }

        try {
            this.renderDialog({
                title: 'Running',
                content: 'It will take few seconds!'
            });
            const kernel: Kernel.IKernelConnection = await NotebookUtils.createNewKernel();
            const args = {
                proxy_url: proxyUrl,
                source_notebook_path: getTransformerNotebookDirectory()
            }
            await executeRpc(kernel, 'proxy.reset', args);
            kernel.shutdown();
            this.renderDialog({
                title: 'Reset is done',
                content: 'You need to reload the page!',
                isCloseButtonVisible: false,
                isConfirmButtonVisible: true
            });
            this.setState({ dialogConfirmClickHandler: this.doReloadPage });
            return;
        } catch (error) {
            globalUnhandledRejection({ reason: error });
            this.renderDialog({
                title: 'Error',
                content: error
            });
            throw error;
        }
    };

    doReloadPage = async () => {
        this.renderDialog({
            visible: false
        });
        window.location.reload();
    };

    onTransformerEnableChanged = (enabled: boolean) => {
        this.setState({ isEnabled: enabled });
        setTransformerEnabled(this.props.transformerSettings, enabled);
    };

    render() {
        return (
            <ThemeProvider theme={theme}>
                <div className={'leftpanel-transformer-widget'} key="transformer-widget" style={{padding: 'var(--jp-code-padding)'}}>
                    <div className={'leftpanel-transformer-widget-content'}>
                        <div className="transformer-header" style={{fontSize: 'var(--jp-ui-font-size3)'}} >
                            <p>Transformer Panel</p>
                        </div>

                        <div className='transformer-component' >
                            <div>
                                <p className="transformer-header" style={{ color: theme.transformer.headers.main, fontSize: 'var(--jp-ui-font-size1)'}}>
                                    Transformer is the extension for model inference, it injects pre and post processors defined in <strong style={{fontSize: 'var(--jp-ui-font-size2)'}}>transformer.ipynb</strong> notebook.
                                </p>
                            </div>
                        </div>

                        <div className="transformer-toggler">
                            <React.Fragment>
                                <div className="toolbar input-container">
                                    <Switch
                                        checked={this.state.isEnabled}
                                        onChange={c => this.onTransformerEnableChanged(c.target.checked)}
                                        color="primary"
                                        name="enable-transformer"
                                        inputProps={{ 'aria-label': 'primary checkbox' }}
                                        classes={{ root: 'material-switch' }}
                                    />
                                    <div className={'switch-label'} style={{ display: 'inline-block' }}>
                                        {(this.state.isEnabled ? 'Disable' : 'Enable') + ' transformer widgets'}
                                    </div>
                                </div>
                            </React.Fragment>
                        </div>

                        <div className={ 'transformer-component' + (this.state.isEnabled ? '' : ' hidden') } style={{ marginTop: '1em' }}>
                            <div>
                                <p className="transformer-header" style={{ color: theme.transformer.headers.main, fontSize: 'var(--jp-ui-font-size1)'}}>
                                    Convert <strong style={{fontSize: 'var(--jp-ui-font-size2)'}}>transformer.ipynb</strong> to runnable python code and apply the pre and post processors for model inference.
                                </p>
                            </div>
                            <div className="input-container add-button">
                                <Button
                                    variant="contained"
                                    color="primary"
                                    size="small"
                                    title="Apply the changes."
                                    onClick={this.applyTransformerToProxy}
                                    disabled={ false }
                                    style={{ marginLeft: '10px', marginTop: '0px' }}
                                >
                                    Apply Transformer
                                </Button>
                            </div>
                        </div>

                        <div className={ 'transformer-component' + (this.state.isEnabled ? '' : ' hidden') } style={{ marginTop: '1em' }}>
                            <div>
                                <p className="transformer-header" style={{ color: theme.transformer.headers.main, fontSize: 'var(--jp-ui-font-size1)'}}>
                                    Reset <strong style={{fontSize: 'var(--jp-ui-font-size2)'}}>transformer.ipynb</strong>, this action also reset the pre and post processors for model inference.
                                </p>
                            </div>
                            <div className="input-container add-button">
                                <Button
                                    variant="contained"
                                    color="secondary"
                                    size="small"
                                    title="Reset Transformer"
                                    onClick={this.resetTransformer}
                                    disabled={ false }
                                    style={{ marginLeft: '10px', marginTop: '0px' }}
                                >
                                    Reset Transformer
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
                <Dialog
                    open={this.state.isDialogVisible}
                    fullWidth={true}
                    maxWidth={'sm'}
                    scroll="paper"
                    aria-labelledby="scroll-dialog-title"
                    aria-describedby="scroll-dialog-description"
                >
                    <DialogTitle id="scroll-dialog-title">
                        <p className={'dialog-title'} >{this.state.dialogTitle}</p>
                    </DialogTitle>
                    <DialogContent dividers={true}>
                        <p>{this.state.dialogContent}</p>
                    </DialogContent>
                    <DialogActions>
                        <Button
                            className={ 'transformer-dialog ' + (this.state.isDialogConfirmButtonVisible ? '' : 'hidden') }
                            color="secondary"
                            onClick={this.state.dialogConfirmClickHandler}
                        >Confirm</Button>
                        <Button
                            className={ 'transformer-dialog ' + (this.state.isDialogCloseButtonVisible ? '' : 'hidden') }
                            color="primary"
                            onClick={this.onDialogCloseClick}
                        >{this.state.closeButtonText}</Button>
                    </DialogActions>
                </Dialog>
            </ThemeProvider>
        );
    }
}
