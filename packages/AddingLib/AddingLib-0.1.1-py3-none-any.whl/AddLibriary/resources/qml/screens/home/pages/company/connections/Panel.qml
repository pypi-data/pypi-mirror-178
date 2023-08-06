import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/js/popups.js" as Popups


Rectangle {
    id: connectionsPanel
    color: ui.colors.dark3
    Layout.alignment: Qt.AlignTop | Qt.AlignLeft
    Layout.fillWidth: true
    Layout.minimumHeight: 112
    Layout.maximumHeight: 112
    Layout.rightMargin: infoConnectionsComponent.visible ? 0 : 8
    property var filters: {"a911_channel_state": new Set([]), "binding_state": new Set([]), "translator_channel_state": new Set([])}
    property var filters_selected: 0
    property var total_counter: 0
    property var counters: {}

    function update_filter() {
        filters["a911_channel_state"] = Array.from(filters["a911_channel_state"])
        filters["binding_state"] = Array.from(filters["binding_state"])
        filters["translator_channel_state"] = Array.from(filters["translator_channel_state"])
        app.company_module.get_company_bindings(filters)
        app.company_module.get_company_bindings_counter(filters)
        filters["a911_channel_state"] = new Set(filters["a911_channel_state"])
        filters["binding_state"] = new Set(filters["binding_state"])
        filters["translator_channel_state"] = new Set(filters["translator_channel_state"])
        infoConnectionsComponent.currentObject = null
        header.Layout.rightMargin = 8
    }

    RowLayout {
        spacing: 24
        width: parent.width - 48
        height: 48
        anchors {
            top: parent.top
            topMargin: 8
            horizontalCenter: parent.horizontalCenter
        }

        Item {
            id: searchItem
            Layout.fillWidth: true
            Layout.minimumHeight: parent.height
            Layout.maximumHeight: parent.height

            Custom.SearchField {
                width: parent.width - 8
                height: 38
                anchors.centerIn: parent
                placeHolderText: tr.connection_search_911

                onReload: {
                    update_filter()
                }

                Keys.onPressed: {
                    if (event.key == Qt.Key_Enter || event.key == Qt.Key_Return) {
                        filters["a911_channel_state"] = Array.from(filters["a911_channel_state"])
                        filters["binding_state"] = Array.from(filters["binding_state"])
                        filters["translator_channel_state"] = Array.from(filters["translator_channel_state"])
                         app.company_module.get_company_binding(control.text, filters)
                        filters["a911_channel_state"] = new Set(filters["a911_channel_state"])
                        filters["binding_state"] = new Set(filters["binding_state"])
                        filters["translator_channel_state"] = new Set(filters["translator_channel_state"])
                        infoConnectionsComponent.currentObject = null
                        header.Layout.rightMargin = 8
                    }
                }
            }
        }

        Item {
            id: addItem
            Layout.alignment: Qt.AlignTop | Qt.AlignRight
            Layout.minimumHeight: parent.height
            Layout.minimumWidth: 220
            Layout.maximumHeight: parent.height
            Layout.maximumWidth: 220
        }
    }

    RowLayout {
        id: tabRow
        spacing: 12
        height: 42

        anchors {
            bottom: parent.bottom
            bottomMargin: 6
            left: parent.left
            leftMargin: 24
        }

        property var currentTab: panelTab

        Item {
            id: panelTab
            property var selected: false

            Layout.minimumHeight: 36
            Layout.maximumHeight: 36
            Layout.minimumWidth: tabText.contentWidth + 24 + chevronImage.width
            Layout.alignment: Qt.AlignBottom | Qt.AlignLeft

            Rectangle {
                width: tabText.contentWidth + chevronImage.width + 12
                height: parent.height
                radius: parent.height / 2
                color: ui.colors.dark4

                Custom.FontText {
                    id: tabText
                    text: tr.connections_filters
                    color: ui.colors.middle1
                    font.pixelSize: 14
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                        leftMargin: 12
                    }
                }

                Image {
                    id: chevronImage
                    source: "qrc:/resources/images/desktop/icons/a-chevron-down.svg"
                    sourceSize.height: 40
                    sourceSize.width: 32

                    anchors {
                        left: tabText.right
                        verticalCenter: parent.verticalCenter
                    }
                }
            }
            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    // app.company_module.get_all_binding_counters()
                    Popups.connections_filter_popup(filters, counters, total_counter)
                }
            }
        }

       Item {
            id: panelTab2
            property var selected: false

            Layout.minimumHeight: 36
            Layout.maximumHeight: 36
            Layout.minimumWidth: reloadItem.width
            Layout.alignment: Qt.AlignBottom | Qt.AlignLeft

            Item {
                id: reloadItem
                width: reloadText.width + reloadImage.width + 2
                height: parent.height
                anchors {
                    right: parent.right
                    top: parent.top
                }

                Image {
                    id: reloadImage
                    source: "qrc:/resources/images/desktop/button_icons/refresh.svg"
                    sourceSize.width: 16
                    sourceSize.height: 16
                    anchors{
                        verticalCenter: parent.verticalCenter
                        left: parent.left
                    }
                }

                Custom.FontText {
                    id: reloadText
                    text: tr.update_911
                    font.pixelSize: 14
                    color: ui.colors.green1

                    anchors {
                        verticalCenter: parent.verticalCenter
                        left: reloadImage.right
                        leftMargin: 2
                    }
                }

                Custom.HandMouseArea {
                    anchors.fill: parent
                    onClicked: {
                        rotAnim.start()
                        update_filter()
                    }
                }

                RotationAnimator {
                    id: rotAnim
                    target: reloadImage;
                    from: 0;
                    to: 360;
                    duration: 500
                    running: false
                }
            }
        }

    }
    Component.onCompleted: {
        update_filter()
        app.company_module.get_all_binding_counters()
    }

    Connections {
        target: app.company_module

        onBindingsCounters: {
            counters = result
        }

        onTotalCounter: {
            total_counter = result
        }

        onUpdateEnded: {
            if (infoConnectionsComponent.currentObject && connectionsList.connectionsData.ownCurrentIndex != -1)
                infoConnectionsComponent.currentObject = appCompany.connections_model.conn_data[connectionsList.connectionsData.ownCurrentIndex]
            else if (infoConnectionsComponent.currentObject && connectionsList.connectionsData.ownCurrentIndex == -1) {
                infoConnectionsComponent.currentObject = null
                header.Layout.rightMargin = 8
            }
        }
    }
}
