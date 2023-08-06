import * as React from 'react';
import CloseIcon from '@material-ui/icons/Close';
import CheckIcon from '@material-ui/icons/Check';
import { IconButton } from '@material-ui/core';
import { Select } from './../components/Select';
import TagsUtils from './../lib/TagsUtils';
import { Notebook, NotebookPanel, NotebookActions } from '@jupyterlab/notebook';
import { Chip, Tooltip } from '@material-ui/core';
import { CellMetadataEditorDialog } from './CellMetadataEditorDialog';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { getTransformerEnabled } from './../settings';
import { fetchTransformerStattes, issueTransformerStatesChange, addStatesChangeListener, ITransformerStates } from './../states'
import { showCurrentActiveCellTransformerWidget } from './../notebook'
import CellUtils from './../lib/CellUtils';
import * as nbformat from '@jupyterlab/nbformat';

const CELL_TYPE_NA = 'na';
const CELL_TYPE_NA_LABEL = '-';

export const CELL_TYPE_PREPROCESSOR = 'preprocessor';
export const CELL_TYPE_POSTPROCESSOR = 'postprocessor';
export const CELL_TYPE_REQUIREMENTS = 'requirements';
export const CELL_TYPE_CVAT_INFO = 'cvat-info';
export const CELL_TYPE_CVAT_PREPROCESSOR = 'cvat-preprocessor';
export const CELL_TYPE_CVAT_POSTPROCESSOR = 'cvat-postprocessor';
const CELL_TYPES: any[] = [
    {
        value: CELL_TYPE_NA,
        label: CELL_TYPE_NA_LABEL,
        helpText: null,
        chipColor: null 
    },
    {
        value: CELL_TYPE_REQUIREMENTS,
        label: 'Requirements',
        helpText: 'The code in this cell will be parsed as requirements packages and install in system.',
        chipColor: 'a32626'
    },
    {
        value: CELL_TYPE_PREPROCESSOR,
        label: 'Pre processor',
        helpText: 'The code in this cell will be parsed as preprocessor for the predict function of deployed model.',
        chipColor: 'ee7a1a'
    },
    {
        value: CELL_TYPE_POSTPROCESSOR,
        label: 'Post processor',
        helpText: 'The code in this cell will be parsed as postprocessor for the predict function of deployed model.',
        chipColor: '773d0d'
    },
    {
        value: 'functions',
        label: 'Extra functions',
        helpText: 'The code in this cell will be parsed as referenced function for the preprocessor or postprocessor.',
        chipColor: 'a32626'
    },
    {
        value: CELL_TYPE_CVAT_INFO,
        label: 'CVAT Info',
        helpText: 'The code in this cell will be parsed as cvat_info callback function.',
        chipColor: 'a32626'
    },
    {
        value: CELL_TYPE_CVAT_PREPROCESSOR,
        label: 'CVAT Pre processor',
        helpText: 'The code in this cell will be parsed as CVAT preprocessor for the predict function of deployed model.',
        chipColor: 'ee7a1a'
    },
    {
        value: CELL_TYPE_CVAT_POSTPROCESSOR,
        label: 'CVAT Post processor',
        helpText: 'The code in this cell will be parsed as CVAT postprocessor for the predict function of deployed model.',
        chipColor: '773d0d'
    }
];

const CELL_TYPE_SELECT_OPTIONS = CELL_TYPES
    //.filter(item => item['value'] !== CELL_TYPE_NA)
    .map(item => {
        const newItem = { ...item };
        delete newItem['helpText'];
        delete newItem.chipColor;
        return newItem;
    });

export const RESERVED_CELL_NAMES: string[] = CELL_TYPES
    .filter(item => item['value'] !== CELL_TYPE_NA)
    .map(item => {
        return item['value'];
    });

export const RESERVED_CELL_NAMES_HELP_TEXT = CELL_TYPES
    .reduce((obj, item) => {
        obj[item.value] = item.helpText;
        return obj;
    } ,{});

export const RESERVED_CELL_NAMES_CHIP_COLOR = CELL_TYPES
    .reduce((obj, item) => {
        obj[item.value] = item.chipColor;
        return obj;
    } ,{});

const PREPROCESSOR_DEF_REGEX = /\s*def\s+preprocess\s*\(\s*\S+\s*(:\s*\S+\s*)*\)\s*(->\s*\S+\s*)*:\s*/i
const PREPROCESSOR_DEFAULT_CODE_SNIPPET = `from typing import Dict
def preprocess(input: Dict) -> Dict:
    return input`

const POSTPROCESSOR_DEF_REGEX = /\s*def\s+postprocess\s*\(\s*\S+\s*(:\s*\S+\s*)*\)\s*(->\s*\S+\s*)*:\s*/i
const POSTPROCESSOR_DEFAULT_CODE_SNIPPET = `from typing import Dict
def postprocess(input: Dict) -> Dict:
    return input`

const CVAT_INFO_DEF_REGEX = /\s*def\s+cvat_info\s*\(\s*\S*\s*(:\s*\S+\s*)*(=\s*('|")*\S+('|")*\s*)*\)\s*(->\s*\S+\s*)*:\s*/i
const CVAT_INFO_DEFAULT_CODE_SNIPPET = `from typing import Dict
def cvat_info(inputs: Dict = None) -> Dict:
    return {
        "framework": "",
        "spec": None,
        "type": "",
        "description": ""
    }`

const CVAT_PREPROCESSOR_DEF_REGEX = /\s*def\s+cvat_preprocess\s*\(\s*\S+\s*(:\s*\S+\s*)*\)\s*(->\s*\S+\s*)*:\s*/i
const CVAT_PREPROCESSOR_DEFAULT_CODE_SNIPPET = `from typing import Dict
def cvat_preprocess(input: Dict) -> Dict:
    return input`

const CVAT_POSTPROCESSOR_DEF_REGEX = /\s*def\s+cvat_postprocess\s*\(\s*\S+\s*(:\s*\S+\s*)*\)\s*(->\s*\S+\s*)*:\s*/i
const CVAT_POSTPROCESSOR_DEFAULT_CODE_SNIPPET = `from typing import Dict
def cvat_postprocess(input: Dict) -> Dict:
    return []`

const enum CellCodeErrors {
  VOID,
  FUNC_DEF_ERROR
}
export interface IProps {
    notebookPanel: NotebookPanel;
    cellElement: any;
    transformerTag?: string;
    transformerSettings?: ISettingRegistry.ISettings;
    isTransformerEnabled?: boolean;
    cellId?: string;
}

interface IState {
    transformerTag?: string;
    isChipVisible?: boolean;
    isSelectorVisible?: boolean;
    cellMetadataEditorDialog?: boolean;
    dialogTitle?: string;
    dialogContent?: string;
    dialogCode?: string;
    isTransformerEnabled: boolean;
    typeSelectOptions: any[];
}

export class CellMetadataEditor extends React.Component<IProps, IState> {
    transformerStates: ITransformerStates = null;

    constructor(props: IProps) {
        super(props);
        this.transformerStates = fetchTransformerStattes();
        this.updateLocalTransformerStates(props.transformerTag, true);
        addStatesChangeListener(this.onStatesChangeCallback);
        issueTransformerStatesChange(this.props.cellId, this.transformerStates);
        const defaultState: IState = {
            transformerTag: props.transformerTag?props.transformerTag : CELL_TYPE_NA,
            isChipVisible: RESERVED_CELL_NAMES.includes(props.transformerTag)? true: false,
            isSelectorVisible: false,
            cellMetadataEditorDialog: false,
            dialogTitle: 'Warning',
            dialogContent: '',
            dialogCode: null,
            isTransformerEnabled: this.props.isTransformerEnabled,
            typeSelectOptions: this.getTypeSelectOptions([props.transformerTag])
        };
        this.state = defaultState;
        this.updateCurrentCellTag = this.updateCurrentCellTag.bind(this);
        this.toggleTagsEditorDialog = this.toggleTagsEditorDialog.bind(this);
        if(this.props.transformerSettings) {
            this.props.transformerSettings.changed.connect(this.updateTransformerEnabled);
        }
    }

    isTagged = (tag: string): boolean => {
        if(tag === CELL_TYPE_PREPROCESSOR) {
            return this.transformerStates.isPreprocessorTagged;
        } else if(tag === CELL_TYPE_POSTPROCESSOR) {
            return this.transformerStates.isPostprocessorTagged;
        } else if(tag === CELL_TYPE_REQUIREMENTS) {
            return this.transformerStates.isRequirementsTagged;
        } else if(tag === CELL_TYPE_CVAT_INFO) {
            return this.transformerStates.isCVATInfoTagged;
        } else if(tag === CELL_TYPE_CVAT_PREPROCESSOR) {
            return this.transformerStates.isCVATPreprocessorTagged;
        } else if(tag === CELL_TYPE_CVAT_POSTPROCESSOR) {
            return this.transformerStates.isCVATPostprocessorTagged;
        }
        return false;
    }

    updateLocalTransformerStates = (tag: string, tagged: boolean): void => {
        if(tag === CELL_TYPE_PREPROCESSOR) {
            this.transformerStates.isPreprocessorTagged = tagged;
        } else if(tag === CELL_TYPE_POSTPROCESSOR) {
            this.transformerStates.isPostprocessorTagged = tagged;
        } else if(tag === CELL_TYPE_REQUIREMENTS) {
            this.transformerStates.isRequirementsTagged = tagged;
        } else if(tag === CELL_TYPE_CVAT_INFO) {
            this.transformerStates.isCVATInfoTagged = tagged;
        } else if(tag === CELL_TYPE_CVAT_PREPROCESSOR) {
            this.transformerStates.isCVATPreprocessorTagged = tagged;
        } else if(tag === CELL_TYPE_CVAT_POSTPROCESSOR) {
            this.transformerStates.isCVATPostprocessorTagged = tagged;
        }
    }

    onStatesChangeCallback = (issuer: string, newStates: ITransformerStates) : void => {
        if(issuer == this.props.cellId) {
            return;
        };
        this.transformerStates = newStates;
        this.setState({typeSelectOptions: this.getTypeSelectOptions([this.state.transformerTag])});
    }

    updateTransformerEnabled = (settings: ISettingRegistry.ISettings): void => {
        this.setState({isTransformerEnabled: getTransformerEnabled()});
    };

    checkCellCodeDefinitionConfirmed = (notebook: Notebook, cellIndex: number, tag: string) => {
        console.log("checkCellCodeDefinitionConfirmed");
        let regex = null;
        if(tag == CELL_TYPE_PREPROCESSOR) {
            regex = PREPROCESSOR_DEF_REGEX;
        } else if(tag == CELL_TYPE_POSTPROCESSOR) {
            regex = POSTPROCESSOR_DEF_REGEX;
        } else if(tag == CELL_TYPE_CVAT_INFO) {
            regex = CVAT_INFO_DEF_REGEX;
        } else if(tag == CELL_TYPE_CVAT_PREPROCESSOR) {
            regex = CVAT_PREPROCESSOR_DEF_REGEX;
        } else if(tag == CELL_TYPE_CVAT_POSTPROCESSOR) {
            regex = CVAT_POSTPROCESSOR_DEF_REGEX;
        }
        if(regex) {
            if(CellUtils.isCellVoid(notebook, cellIndex)) {
                return {
                    confirmed: false,
                    error: CellCodeErrors.VOID
                }
            } else if(! CellUtils.isTextInCell(notebook, cellIndex, regex)) {
                return {
                    confirmed: false,
                    error: CellCodeErrors.FUNC_DEF_ERROR
                }
            }
        }

        return {
            confirmed: true
        }
    }

    updateCurrentCellTag = async (value: string) => {
        if(value !== this.state.transformerTag) {
            this.updateLocalTransformerStates(this.state.transformerTag, false);
            this.updateLocalTransformerStates(value, true);
            issueTransformerStatesChange(this.props.cellId, this.transformerStates);
            if (RESERVED_CELL_NAMES.includes(value)) {
                this.setState({ transformerTag: value });
            } else if(CELL_TYPE_NA === value) {
                this.setState({ transformerTag: CELL_TYPE_NA });
            }

            let notebook: Notebook = this.props.notebookPanel.content;
            let currentCellType: string = this.props.notebookPanel.model.cells.get(notebook.activeCellIndex).type;
            let targetCellType: string = currentCellType;
            if(value == CELL_TYPE_PREPROCESSOR || value == CELL_TYPE_POSTPROCESSOR || value == CELL_TYPE_CVAT_INFO || value == CELL_TYPE_CVAT_PREPROCESSOR || value == CELL_TYPE_CVAT_POSTPROCESSOR) {
                let confirmedResult = this.checkCellCodeDefinitionConfirmed(notebook, notebook.activeCellIndex, value);
                if(! confirmedResult.confirmed) {
                    let codeSnippet = PREPROCESSOR_DEFAULT_CODE_SNIPPET;
                    if(value == CELL_TYPE_POSTPROCESSOR) {
                        codeSnippet = POSTPROCESSOR_DEFAULT_CODE_SNIPPET;
                    } else if(value == CELL_TYPE_CVAT_INFO) {
                        codeSnippet = CVAT_INFO_DEFAULT_CODE_SNIPPET;
                    } else if(value == CELL_TYPE_CVAT_PREPROCESSOR) {
                        codeSnippet = CVAT_PREPROCESSOR_DEFAULT_CODE_SNIPPET;
                    } else if(value == CELL_TYPE_CVAT_POSTPROCESSOR) {
                        codeSnippet = CVAT_POSTPROCESSOR_DEFAULT_CODE_SNIPPET;
                    }
                    if(confirmedResult.error == CellCodeErrors.VOID) {
                        CellUtils.injectCodeAtIndex(notebook, notebook.activeCellIndex, codeSnippet);
                    } else if(confirmedResult.error == CellCodeErrors.FUNC_DEF_ERROR) {
                        let dialogTitle = "Function %s is not well defined!".replace(/%s/i, value);
                        let dialogContent = "Please define function %s as follows:".replace(/%s/i, value);
                        this.setState({
                            dialogTitle: dialogTitle,
                            dialogContent: dialogContent,
                            dialogCode: codeSnippet
                        });
                        this.toggleTagsEditorDialog();
                    }
                }
                targetCellType = 'code';
            } else if(value == CELL_TYPE_REQUIREMENTS) {
                targetCellType = 'raw';
            }

            if(currentCellType != targetCellType) {
                console.log("Keep transformer metadata in cell metadata and replace cell widget...");
                let cellMetadata = {
                    transformerTag: value,
                };
                TagsUtils.setCellTransformerTag(
                    this.props.notebookPanel,
                    notebook.activeCellIndex,
                    cellMetadata,
                    false
                ).then(newValue => {
                    NotebookActions.changeCellType(notebook, targetCellType as nbformat.CellType);
                    showCurrentActiveCellTransformerWidget(this.props.notebookPanel);
                });
            }
        }
    };

    saveCellTagInNotebookFile = () => {
        console.log("saveCellTagInNotebookFile");
        let value = this.state.transformerTag;

            if(value == CELL_TYPE_PREPROCESSOR || value == CELL_TYPE_POSTPROCESSOR || value == CELL_TYPE_CVAT_INFO || value == CELL_TYPE_CVAT_PREPROCESSOR || value == CELL_TYPE_CVAT_POSTPROCESSOR) {
            let notebook: Notebook = this.props.notebookPanel.content;
            let confirmedResult = this.checkCellCodeDefinitionConfirmed(notebook, notebook.activeCellIndex, value);
            if(! confirmedResult.confirmed) {
                if(confirmedResult.error == CellCodeErrors.VOID) {
                    let dialogTitle = "Function %s is void!".replace(/%s/i, value);
                    let dialogContent = "Unable to apply the function %s defined here!".replace(/%s/i, value);
                    this.setState({
                        dialogTitle: dialogTitle,
                        dialogContent: dialogContent,
                        dialogCode: null
                    });
                    this.toggleTagsEditorDialog();
                    return;
                }
                if(confirmedResult.error == CellCodeErrors.FUNC_DEF_ERROR) {
                    let codeSnippet = PREPROCESSOR_DEFAULT_CODE_SNIPPET;
                    if(value == CELL_TYPE_POSTPROCESSOR) {
                        codeSnippet = POSTPROCESSOR_DEFAULT_CODE_SNIPPET;
                    } else if(value == CELL_TYPE_CVAT_INFO) {
                        codeSnippet = CVAT_INFO_DEFAULT_CODE_SNIPPET;
                    } else if(value == CELL_TYPE_CVAT_PREPROCESSOR) {
                        codeSnippet = CVAT_PREPROCESSOR_DEFAULT_CODE_SNIPPET;
                    } else if(value == CELL_TYPE_CVAT_POSTPROCESSOR) {
                        codeSnippet = CVAT_POSTPROCESSOR_DEFAULT_CODE_SNIPPET;
                    }
                    let dialogTitle = "Function %s is not well defined!".replace(/%s/i, value);
                    let dialogContent = "Please define function %s as follows:".replace(/%s/i, value);
                    this.setState({
                        dialogTitle: dialogTitle,
                        dialogContent: dialogContent,
                        dialogCode: codeSnippet
                    });
                    this.toggleTagsEditorDialog();
                    return;
                }
            }
        }

        let isDuplicated = false;
        if(value == CELL_TYPE_PREPROCESSOR || value == CELL_TYPE_POSTPROCESSOR || value == CELL_TYPE_CVAT_INFO || value == CELL_TYPE_CVAT_PREPROCESSOR || value == CELL_TYPE_CVAT_POSTPROCESSOR) {
            isDuplicated = TagsUtils.isTransformerTagExistedInOtherCells(
                this.props.notebookPanel,
                this.props.notebookPanel.content.activeCellIndex,
                value
            );
        }

        if(isDuplicated) {
            this.setState({
                dialogTitle: "Error",
                dialogContent: value + " is limited to be just one.",
                dialogCode: null
            });
            this.toggleTagsEditorDialog();
        } else {
            if (RESERVED_CELL_NAMES.includes(value)) {
                let cellMetadata = {
                    transformerTag: value,
                };
                TagsUtils.setCellTransformerTag(
                    this.props.notebookPanel,
                    this.props.notebookPanel.content.activeCellIndex,
                    cellMetadata
                ).then(newValue => {
                    this.hideSelector();
                });
            } else if(CELL_TYPE_NA === value) {
                TagsUtils.resetCellTransformerTag(
                    this.props.notebookPanel,
                    this.props.notebookPanel.content.activeCellIndex,
                ).then(newValue => {
                    this.hideSelector();
                });
            }
        }
    }

    removeCellTagInNotebookFile = () => {
        this.updateLocalTransformerStates(this.state.transformerTag, false);
        issueTransformerStatesChange(this.props.cellId, this.transformerStates);
        TagsUtils.resetCellTransformerTag(
            this.props.notebookPanel,
            this.props.notebookPanel.content.activeCellIndex,
        ).then(newValue => {
            // update transformerTag state HERE to avoid a tricky issue
            this.setState({ transformerTag: CELL_TYPE_NA });
            this.hideSelector();
        });
    }

    isEqual(a: any, b: any): boolean {
        return JSON.stringify(a) === JSON.stringify(b);
    }

    componentDidUpdate(prevProps: Readonly<IProps>, prevState: Readonly<IState>) {
        this.hideEditorIfNotCodeCell();
    }

    hideEditorIfNotCodeCell() {
    }

    static getDerivedStateFromProps (props: IProps, state: IState) : any {
        return null;
    }

    onBeforeUpdate = (value: string) => {
        if (value === this.props.transformerTag) {
            return false;
        }
        return false;
    };

    toggleSelector() {
        if(this.state.isSelectorVisible) {
            this.hideSelector();
        } else {
            this.showSelector();
        }
    }

    showSelector() {
        this.setState({
            isSelectorVisible: true,
            isChipVisible: false
        });
    }

    hideSelector() {
        this.setState({
            isSelectorVisible: false,
            isChipVisible: RESERVED_CELL_NAMES.includes(this.state.transformerTag)? true : false
        });
    }

    onChipClick() {
        this.setState({ isSelectorVisible: true, isChipVisible: false });
    }

    toggleTagsEditorDialog() {
        this.setState({ cellMetadataEditorDialog: !this.state.cellMetadataEditorDialog });
    }

    componentDidMount = () => {
    };

    getTypeSelectOptions = (keepTags: string[]): any[] => {
        return CELL_TYPE_SELECT_OPTIONS
        .filter(item => (keepTags.includes(item['value']) || !this.isTagged(item['value'])))
        .map(item => {
            const newItem = { ...item };
            delete newItem['helpText'];
            delete newItem.chipColor;
            return newItem;
        });
    }

    render() {
        const cellTag = RESERVED_CELL_NAMES.includes(this.state.transformerTag)? this.state.transformerTag : 'na';
        const cellColor = 'transparent';

        // add class names for styling
        if(! this.state.isTransformerEnabled) {
            this.props.cellElement.classList.remove('with-transformer-editor');
            this.props.cellElement.classList.remove('with-transformer-chip');
        } else if(this.state.isSelectorVisible) {
            this.props.cellElement.classList.add('with-transformer-editor');
            this.props.cellElement.classList.remove('with-transformer-chip');
        } else if(this.state.isChipVisible) {
            this.props.cellElement.classList.remove('with-transformer-editor');
            this.props.cellElement.classList.add('with-transformer-chip');
        } else {
            this.props.cellElement.classList.remove('with-transformer-editor');
            this.props.cellElement.classList.remove('with-transformer-chip');
        }

        return (
            <React.Fragment>
                <div className={ 'transformer-inline-cell-metadata' + ((this.state.isTransformerEnabled && this.state.isChipVisible)? '' : ' hidden') }>
                    <Tooltip
                        placement="top"
                        key={this.state.transformerTag + 'tooltip'}
                        title={
                            RESERVED_CELL_NAMES.includes(this.state.transformerTag)?
                            RESERVED_CELL_NAMES_HELP_TEXT[this.state.transformerTag] :
                            'This cell starts the pipeline step: ' + this.state.transformerTag
                        }
                    >
                        <Chip
                            className={ 'transformer-meta-chip' }
                            key={ this.state.transformerTag }
                            label={ this.state.transformerTag }
                            onClick={() => this.onChipClick()}
                        />
                    </Tooltip>
                </div>
                <div className={ 'transformer-metadata-editor-wrapper' + ((this.state.isTransformerEnabled && this.state.isSelectorVisible)? '' : ' hidden') }>
                    <div
                        className={ 'transformer-cell-metadata-editor' }
                        style={{ borderLeft: `2px solid ${cellColor}` }}
                    >
                        <Select
                            updateValue={this.updateCurrentCellTag}
                            values={this.state.typeSelectOptions}
                            value={cellTag}
                            label={'Cell tag'}
                            index={0}
                            variant="outlined"
                            style={{ width: 'auto', minWidth: '14em' }}
                        />
                        <IconButton
                            aria-label="remove"
                            onClick={() => this.removeCellTagInNotebookFile()}
                        >
                            <CloseIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                            aria-label="apply"
                            onClick={() => this.saveCellTagInNotebookFile()}
                        >
                            <CheckIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                            className={ 'transformer-cell-metadata-editor-toggle' }
                            aria-label="toggle"
                            onClick={() => this.toggleSelector()}
                            style={{ width: '0', height: '0', padding: '0' }}
                        />
                    </div>
                    <div className={ 'transformer-cell-metadata-editor-helper-text' + (this.state.isSelectorVisible ? '' : ' hidden') }>
                    </div>
                </div>
                <CellMetadataEditorDialog
                    open={this.state.cellMetadataEditorDialog}
                    toggleDialog={this.toggleTagsEditorDialog}
                    title={this.state.dialogTitle}
                    content={this.state.dialogContent}
                    code={this.state.dialogCode}
                />
            </React.Fragment>
        );
    }
}
