import React, { useReducer } from "react";
import AceEditor from "react-ace";
import { renderValue } from "./MarkedMustache";

import "ace-builds/src-noconflict/mode-markdown";
import "ace-builds/src-noconflict/mode-json";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-searchbox";

import { DataTable, View } from "@mwdb-web/commons/ui";
import exampleTemplates, { makeContext } from "./exampleTemplates";

function templateReducer(state, action) {
    console.log(state, action);
    if (action.type === "edit") {
        if (state.chosenExample === "custom") {
            // Editing custom template
            return {
                ...state,
                templateInput:
                    action.templateInput !== undefined
                        ? action.templateInput
                        : state.templateInput,
                valueInput:
                    action.valueInput !== undefined
                        ? action.valueInput
                        : state.valueInput,
            };
        } else {
            // Editing chosen example, apply secondary field from the chosen template
            return {
                chosenExample: "custom", // go to custom mode
                templateInput:
                    action.templateInput !== undefined
                        ? action.templateInput
                        : exampleTemplates[state.chosenExample].template,
                valueInput:
                    action.valueInput !== undefined
                        ? action.valueInput
                        : exampleTemplates[state.chosenExample].value,
            };
        }
    } else if (action.type === "choose") {
        // New example chosen. Remember custom fields but show new example
        return {
            ...state,
            chosenExample: action.chosenExample,
        };
    }
}

export default function RichAttributePreview({
    storedRichTemplate,
    storedExampleValue,
    onStore,
    onCancel,
    onDelete,
}) {
    const [templateState, dispatch] = useReducer(templateReducer, {
        chosenExample: "custom",
        templateInput: storedRichTemplate,
        valueInput: storedExampleValue,
    });

    function chooseTemplate(ev) {
        const index = ev.target.value;
        dispatch({ type: "choose", chosenExample: index });
    }

    function editTemplate(field, newValue) {
        dispatch({ type: "edit", [field]: newValue });
    }

    const template =
        templateState.chosenExample !== "custom"
            ? exampleTemplates[templateState.chosenExample].template
            : templateState.templateInput;
    const value =
        templateState.chosenExample !== "custom"
            ? exampleTemplates[templateState.chosenExample].value
            : templateState.valueInput;
    let renderedValue,
        invalid = false;
    try {
        renderedValue = renderValue(template, makeContext(JSON.parse(value)));
    } catch (e) {
        renderedValue = e.toString();
        invalid = true;
    }

    return (
        <View ident="attributePreview">
            <select
                className="custom-select"
                value={templateState.chosenExample}
                onChange={chooseTemplate}
            >
                <option value="custom">(custom template)</option>
                {exampleTemplates.map((value, index) => (
                    <option value={index}>{value.name}</option>
                ))}
            </select>
            <div className="row">
                <div className="col-6">
                    <strong>Template</strong>
                    <AceEditor
                        mode="markdown"
                        theme="github"
                        value={template}
                        wrapEnabled
                        width="100%"
                        fontSize="16px"
                        onChange={(newTemplate) => {
                            editTemplate("templateInput", newTemplate);
                        }}
                        setOptions={{
                            useWorker: false,
                        }}
                    />
                </div>
                <div className="col-6">
                    <strong>Example value</strong>
                    <AceEditor
                        mode="json"
                        theme="github"
                        value={value}
                        wrapEnabled
                        width="100%"
                        fontSize="16px"
                        onChange={(newValue) => {
                            editTemplate("valueInput", newValue);
                        }}
                        setOptions={{
                            useWorker: false,
                        }}
                    />
                </div>
            </div>
            <div className="row">
                <div className="col">
                    <strong>Preview</strong>
                    <DataTable>
                        <tr>
                            <th>My attribute</th>
                            <td>{renderedValue}</td>
                        </tr>
                    </DataTable>
                </div>
            </div>
            <div className="btn-group">
                <button
                    type="button"
                    className="btn btn-success mr-1"
                    disabled={invalid}
                    onClick={(e) => {
                        if (!invalid) onStore(template, value);
                    }}
                >
                    Store
                </button>
                <button
                    type="button"
                    className="btn btn-danger mr-1"
                    onClick={() => onCancel()}
                >
                    Cancel
                </button>
                <button
                    type="button"
                    className="btn btn-light mr-1"
                    onClick={() => onDelete()}
                >
                    Clear
                </button>
            </div>
        </View>
    );
}
