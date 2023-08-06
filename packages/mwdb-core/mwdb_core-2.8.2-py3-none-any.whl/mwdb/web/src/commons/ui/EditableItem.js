import React, { useState } from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes, faEdit, faSave } from "@fortawesome/free-solid-svg-icons";

function EditButton({ onClick }) {
    return (
        <button
            className="float-right align-middle btn shadow-none"
            style={{ cursor: "pointer" }}
            type="button"
            onClick={onClick}
        >
            <small className="text-muted">Edit </small>
            <FontAwesomeIcon icon={faEdit} />
        </button>
    );
}

export function EditableItem({
    name,
    type,
    selective,
    badge,
    children,
    defaultValue,
    onSubmit,
    masked,
    ...props
}) {
    const [value, setValue] = useState(defaultValue);
    const [edit, setEdit] = useState(false);

    return (
        <form
            onSubmit={(ev) => {
                ev.preventDefault();
                onSubmit({ [name]: value });
                setEdit(false);
            }}
        >
            {edit ? (
                <div className="input-group">
                    {selective ? (
                        <select
                            className="form-control"
                            value={value}
                            name={name}
                            onChange={(ev) => setValue(ev.target.value)}
                            {...props}
                        >
                            {children}
                        </select>
                    ) : (
                        <input
                            type={type || "text"}
                            name={name}
                            className="form-control"
                            value={value}
                            onChange={(ev) => setValue(ev.target.value)}
                            {...props}
                        />
                    )}
                    <div className="input-group-append">
                        <button
                            className="btn btn-outline-success"
                            type="submit"
                        >
                            <small>Save </small>
                            <FontAwesomeIcon icon={faSave} />
                        </button>
                        <button
                            className="btn btn-outline-danger"
                            type="button"
                            onClick={() => {
                                setValue(defaultValue);
                                setEdit(false);
                            }}
                        >
                            <small>Cancel </small>
                            <FontAwesomeIcon icon={faTimes} />
                        </button>
                    </div>
                </div>
            ) : (
                <div>
                    <span
                        className={
                            badge
                                ? "badge badge-secondary align-middle"
                                : "align-middle"
                        }
                    >
                        {masked ? (
                            <span>{"•".repeat(defaultValue.length)}</span>
                        ) : (
                            <span>{defaultValue}</span>
                        )}
                    </span>
                    <EditButton
                        onClick={(ev) => {
                            ev.preventDefault();
                            setValue(defaultValue);
                            setEdit(true);
                        }}
                    />
                </div>
            )}
        </form>
    );
}

export function PseudoEditableItem({ children, editLocation }) {
    /*
     Looks the same as regular editable item, but Edit button redirects to the
     separate editing view
     */
    return (
        <div>
            <span className="align-middle">{children}</span>
            <Link to={editLocation}>
                <EditButton />
            </Link>
        </div>
    );
}
