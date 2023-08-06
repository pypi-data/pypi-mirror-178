import React from "react";

export { default as Autocomplete } from "./Autocomplete";
export { default as BootstrapSelect } from "./BootstrapSelect";
export { default as ConfirmationModal } from "./ConfirmationModal";
export { default as DataTable } from "./DataTable";
export { default as DateString } from "./DateString";
export { EditableItem, PseudoEditableItem } from "./EditableItem";
export {
    default as ErrorBoundary,
    Alert,
    getErrorMessage,
} from "./ErrorBoundary";
export { default as FeatureSwitch } from "./FeatureSwitch";
export { default as GroupBadge, UserBadge } from "./GroupBadge";
export { default as Hash } from "./Hash";
export { default as HexView } from "./HexView";
export { default as Identicon } from "./Identicon";
export { default as NavDropdown } from "./NavDropdown";
export { default as ObjectLink } from "./ObjectLink";
export { default as PagedList } from "./PagedList";
export { default as ShareReasonString } from "./ShareReasonString";
export { default as SortedList } from "./SortedList";
export { default as View, useViewAlert } from "./View";
export { default as ActionCopyToClipboard } from "./ActionCopyToClipboard";
export { RequiresAuth, RequiresCapability } from "./RequiresAuth";

export { Tag, TagList, getStyleForTag } from "./Tag";
export {
    TabContext,
    useTabContext,
    ObjectTab,
    ObjectAction,
} from "./ObjectTab";

export function ShowIf({ condition, children }) {
    return condition ? children : [];
}

export function LimitTo({ children, count }) {
    const more =
        children.length > count
            ? [
                  <small className="text-muted">
                      {" "}
                      and {children.length - 5} more
                  </small>,
              ]
            : [];
    return [...children.slice(0, count), ...more];
}

export function HighlightText(props) {
    let text = React.Children.toArray(props.children)[0].toString();

    if (!props.filterValue) return text;

    let filteredText = props.caseSensitive ? text : text.toLowerCase();
    let filterValue = props.caseSensitive
        ? props.filterValue
        : props.filterValue.toLowerCase();
    let elements = [];

    for (
        var prevIndex = 0, index = filteredText.indexOf(filterValue);
        index >= 0;
        prevIndex = index + filterValue.length,
            index = filteredText.indexOf(
                filterValue,
                index + filterValue.length
            )
    ) {
        elements = elements.concat([
            text.slice(prevIndex, index),
            <span style={{ backgroundColor: "yellow" }}>
                {text.slice(index, index + filterValue.length)}
            </span>,
        ]);
    }
    elements.push(text.slice(prevIndex));
    return elements;
}
