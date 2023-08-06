import React, { useContext } from "react";
import { Link, useParams } from "react-router-dom";

import {
    ShowObject,
    ObjectTab,
    ObjectContext,
    LatestConfigTab,
    RelationsTab,
    DownloadAction,
    FavoriteAction,
    RemoveAction,
    ObjectAction,
    PushAction,
    PullAction,
} from "./ShowObject";

import {
    faScroll,
    faFingerprint,
    faRandom,
    faSearch,
} from "@fortawesome/free-solid-svg-icons";

import {
    makeSearchLink,
    makeSearchDateLink,
    downloadData,
    humanFileSize,
} from "@mwdb-web/commons/helpers";
import { DataTable, DateString, HexView } from "@mwdb-web/commons/ui";
import { Extendable } from "@mwdb-web/commons/extensions";
import { useRemotePath } from "@mwdb-web/commons/remotes";

function TextBlobDetails() {
    const context = useContext(ObjectContext);
    const remotePath = useRemotePath();
    return (
        <DataTable>
            <Extendable ident="showTextBlobDetails">
                <tr>
                    <th>Blob name</th>
                    <td id="blob_name">
                        <Link
                            to={makeSearchLink({
                                field: "name",
                                value: context.object.blob_name,
                                pathname: `${remotePath}/blobs`,
                            })}
                        >
                            {context.object.blob_name}
                        </Link>
                    </td>
                </tr>
                <tr>
                    <th>Blob size</th>
                    <td id="blob_size">
                        <Link
                            to={makeSearchLink({
                                field: "size",
                                value: context.object.blob_size,
                                pathname: `${remotePath}/blobs`,
                            })}
                        >
                            {humanFileSize(context.object.blob_size)}
                        </Link>
                    </td>
                </tr>
                <tr>
                    <th>Blob type</th>
                    <td id="blob_type">
                        <Link
                            to={makeSearchLink({
                                field: "type",
                                value: context.object.blob_type,
                                pathname: `${remotePath}/blobs`,
                            })}
                        >
                            {context.object.blob_type}
                        </Link>
                    </td>
                </tr>
                <tr>
                    <th>First seen</th>
                    <td id="upload_time">
                        {" "}
                        {context.object.upload_time ? (
                            <Link
                                to={makeSearchDateLink({
                                    field: "upload_time",
                                    value: context.object.upload_time,
                                    pathname: `${remotePath}/blobs`,
                                })}
                            >
                                <DateString date={context.object.upload_time} />
                            </Link>
                        ) : (
                            []
                        )}
                    </td>
                </tr>
                <tr>
                    <th>Last seen</th>
                    <td id="last_seen">
                        {" "}
                        {context.object.last_seen ? (
                            <Link
                                to={makeSearchDateLink({
                                    field: "last_seen",
                                    value: context.object.last_seen,
                                    pathname: `${remotePath}/blobs`,
                                })}
                            >
                                <DateString date={context.object.last_seen} />
                            </Link>
                        ) : (
                            []
                        )}
                    </td>
                </tr>
            </Extendable>
        </DataTable>
    );
}

function TextBlobPreview() {
    const context = useContext(ObjectContext);
    return (
        <HexView content={context.object.content} mode="raw" showInvisibles />
    );
}

function BlobDiffAction() {
    const context = useContext(ObjectContext);
    const remotePath = useRemotePath();
    return (
        <ObjectAction
            label="Diff with"
            icon={faRandom}
            link={`${remotePath}/blobs?diff=${context.object.id}`}
        />
    );
}

export default function ShowTextBlob(props) {
    const params = useParams();
    const remotePath = useRemotePath();
    async function downloadTextBlob(object) {
        downloadData(object.content, object.id, "text/plain");
    }

    return (
        <ShowObject
            ident="showTextBlob"
            objectType="blob"
            objectId={params.hash}
            searchEndpoint={`${remotePath}/blobs`}
            headerIcon={faScroll}
            headerCaption="Blob details"
            defaultTab="preview"
        >
            <ObjectTab
                tab="details"
                icon={faFingerprint}
                component={TextBlobDetails}
                actions={[
                    <RemoveAction />,
                    <PushAction />,
                    <PullAction />,
                    <BlobDiffAction />,
                    <FavoriteAction />,
                    <DownloadAction download={downloadTextBlob} />,
                ]}
            />
            <RelationsTab />
            <ObjectTab
                tab="preview"
                icon={faSearch}
                component={TextBlobPreview}
                actions={[
                    <RemoveAction />,
                    <PushAction />,
                    <PullAction />,
                    <BlobDiffAction />,
                    <FavoriteAction />,
                    <DownloadAction download={downloadTextBlob} />,
                ]}
            />
            <LatestConfigTab label="Parsed blob" />
        </ShowObject>
    );
}
