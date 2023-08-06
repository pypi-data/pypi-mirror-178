import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"


Popup {
    id: popup

    width: {
        let diff  = rowlauyottt.width - 634
        return 715 + diff
    }
    height: 341
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    focus: true
    modal: false

    anchors.centerIn: null
    parent: ApplicationWindow.contentItem

    x: 352
    y: 172

    property var counters: {"total": 0, "hub_company_binding": {"approved": 0, "pending_approval": 0, "pending_deletion": 0}, "a911_channel": {"active": 0, "inactive": 0, "pending_removal": 0}, "translator_channel": {"inactive": 0, "active": 0}}
    property var filters_selected: {"911": 0, "translator": 0, "binding": 0}
    property var filters: {"a911_channel_state": new Set([]), "binding_state": new Set([]), "translator_channel_state": new Set([])}
    property var total_counter: -1

    background: Rectangle {
        color: "transparent"
        width: popup.width
        height: popup.height
        x: parent.x
        y: parent.y
    }

    contentItem: Rectangle {
        color: ui.colors.dark2
        width: popup.width
        height: popup.height
        x: parent.x
        y: parent.y
        radius: 8

        ColumnLayout {
            anchors {
                top: parent.top
                left: parent.left
                bottom: parent.bottom
                leftMargin: 32
                topMargin: 32
            }
            spacing: 8

            Item {
                id: first
                Layout.fillWidth: true
                height: label_911.height

                Custom.FontText {
                    id: label_911
                    font.pixelSize: 14
                    text: tr.a911_binding_status
                    color: ui.colors.light3
                }
            }

            RowLayout {
                Layout.fillWidth: true
                height: 32
                spacing: 14
                Layout.alignment: Qt.AlignTop

                EventTypeButton {
                    id: all_911_filter
                    height: 32
                    selected: filters["a911_channel_state"].size == 0
                    text: tr.a911_all + " · " + counters["total"]

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            inactive_911_filter.selected = false
                            active_911_filter.selected = false
                            deletion_911_filter.selected = false
                            filters["a911_channel_state"].clear()
                            filters_selected["911"] = 0
                            tabText.text = tr.connections_filters
                            if (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"] > 0)
                                tabText.text = tabText.text + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }

                EventTypeButton {
                    id: inactive_911_filter
                    height: 32
                    selected: filters["a911_channel_state"].has(1)
                    text: tr.no_object_911 + " · " + counters["a911_channel"]["inactive"]

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            all_911_filter.selected = false
                            filters["a911_channel_state"].add(1)
                            update_filter()
                            filters_selected["911"] += 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                        } else if (deletion_911_filter.selected || active_911_filter.selected) {
                            selected = !selected
                            filters["a911_channel_state"].delete(1)
                            filters_selected["911"] -= 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }

                EventTypeButton {
                    id: active_911_filter
                    height: 32
                    selected: filters["a911_channel_state"].has(2)
                    text: tr.binding_status_active + " · " + counters["a911_channel"]["active"]
                    color: ui.colors.green1

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            all_911_filter.selected = false
                            filters["a911_channel_state"].add(2)
                            filters_selected["911"] += 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        } else if (deletion_911_filter.selected || inactive_911_filter.selected) {
                            selected = !selected
                            filters["a911_channel_state"].delete(2)
                            filters_selected["911"] -= 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }

                EventTypeButton {
                    id: deletion_911_filter
                    height: 32
                    selected: filters["a911_channel_state"].has(3)
                    text: tr.binding_status_pending_deletion + " · " + counters["a911_channel"]["pending_removal"]
                    color: ui.colors.red1

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            all_911_filter.selected = false
                            filters["a911_channel_state"].add(3)
                            filters_selected["911"] += 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        } else if (active_911_filter.selected || inactive_911_filter.selected) {
                            selected = !selected
                            filters["a911_channel_state"].delete(3)
                            filters_selected["911"] -= 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }
            }

            Item {
                id: second
                Layout.fillWidth: true
                height: label_translator.height

                Custom.FontText {
                    id: label_translator
                    font.pixelSize: 14
                    text: tr.translator_binding_status
                    color: ui.colors.light3
                }
            }

            RowLayout {
                Layout.fillWidth: true
                height: 32
                spacing: 14
                Layout.alignment: Qt.AlignTop

                EventTypeButton {
                    id: all_translator_filter
                    height: 32
                    selected: filters["translator_channel_state"].size == 0
                    text: tr.a911_all + " · " + counters["total"]

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            inactive_translator_filter.selected = false
                            active_translator_filter.selected = false
                            filters["translator_channel_state"].clear()
                            filters_selected["translator"] = 0
                            tabText.text = tr.connections_filters
                            if (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"] > 0)
                                tabText.text = tabText.text + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }

                EventTypeButton {
                    id: inactive_translator_filter
                    height: 32
                    selected: filters["translator_channel_state"].has(1)
                    text: tr.no_object_911 + " · " + counters["translator_channel"]["inactive"]

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            all_translator_filter.selected = false
                            filters["translator_channel_state"].add(1)
                            filters_selected["translator"] += 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        } else if (active_translator_filter.selected) {
                            selected = !selected
                            filters["translator_channel_state"].delete(1)
                            filters_selected["translator"] -= 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }

                EventTypeButton {
                    id: active_translator_filter
                    height: 32
                    selected: filters["translator_channel_state"].has(2)
                    text: tr.binding_status_active + " · " + counters["translator_channel"]["active"]
                    color: ui.colors.green1

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            all_translator_filter.selected = false
                            filters["translator_channel_state"].add(2)
                            filters_selected["translator"] += 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        } else if (inactive_translator_filter.selected) {
                            selected = !selected
                            filters["translator_channel_state"].delete(2)
                            filters_selected["translator"] -= 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }
            }

            Item {
                id: third
                Layout.fillWidth: true
                height: label_binding.height

                Custom.FontText {
                    id: label_binding
                    font.pixelSize: 14
                    text: tr.binding_911
                    color: ui.colors.light3
                }
            }

            RowLayout {
                id: rowlauyottt
                Layout.fillWidth: true
                height: 32
                spacing: 14
                Layout.alignment: Qt.AlignTop

                EventTypeButton {
                    id: all_binding_filter
                    height: 32
                    selected: filters["binding_state"].size == 0
                    text: tr.a911_all + " · " + counters["total"]

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            pending_binding_filter.selected = false
                            approved_binding_filter.selected = false
                            deletion_binding_filter.selected = false
                            filters["binding_state"].clear()
                            filters_selected["binding"] = 0
                            tabText.text = tr.connections_filters
                            if (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"] > 0)
                                tabText.text = tabText.text + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }

                EventTypeButton {
                    id: pending_binding_filter
                    height: 32
                    selected: filters["binding_state"].has(1)
                    text: tr.binding_status_pending_approval + " · " + counters["hub_company_binding"]["pending_approval"]

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            all_binding_filter.selected = false
                            filters["binding_state"].add(1)
                            filters_selected["binding"] += 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        } else if (deletion_binding_filter.selected || approved_binding_filter.selected) {
                            selected = !selected
                            filters["binding_state"].delete(1)
                            filters_selected["binding"] -= 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }

                EventTypeButton {
                    id: approved_binding_filter
                    height: 32
                    selected: filters["binding_state"].has(2)
                    text: tr.binding_status_approver + " · " + counters["hub_company_binding"]["approved"]
                    color: ui.colors.green1

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            all_binding_filter.selected = false
                            filters["binding_state"].add(2)
                            filters_selected["binding"] += 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        } else if (deletion_binding_filter.selected || pending_binding_filter.selected) {
                            selected = !selected
                            filters["binding_state"].delete(2)
                            filters_selected["binding"] -= 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }

                EventTypeButton {
                    id: deletion_binding_filter
                    height: 32
                    selected: filters["binding_state"].has(3)
                    text: tr.binding_status_pending_deletion + " · " + counters["hub_company_binding"]["pending_deletion"]
                    color: ui.colors.red1

                    typeArea.onClicked: {
                        if (!selected) {
                            selected = !selected
                            all_binding_filter.selected = false
                            filters["binding_state"].add(3)
                            filters_selected["binding"] += 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        } else if (approved_binding_filter.selected || pending_binding_filter.selected) {
                            selected = !selected
                            filters["binding_state"].delete(3)
                            filters_selected["binding"] -= 1
                            tabText.text =  tr.connections_filters + " · " + (filters_selected["911"] + filters_selected["translator"] + filters_selected["binding"])
                            update_filter()
                        }
                    }
                }
            }
            Rectangle {
                width: popup.width - 80
                height: 1
                color: ui.colors.white
                opacity: 0.1
            }
            Item {
                height: 64
                Layout.fillWidth: true

                Custom.FontText {
                    text: tr.reset_connections_filter
                    color: ui.colors.white
                    font.pixelSize: 14
                    anchors.verticalCenter: parent.verticalCenter

                    Custom.HandMouseArea {
                        onClicked: {
                            all_binding_filter.selected = true
                            all_translator_filter.selected = true
                            all_911_filter.selected = true
                            inactive_911_filter.selected = false
                            active_911_filter.selected = false
                            deletion_911_filter.selected = false
                            inactive_translator_filter.selected = false
                            active_translator_filter.selected = false
                            pending_binding_filter.selected = false
                            approved_binding_filter.selected = false
                            deletion_binding_filter.selected = false
                            filters_selected["911"] = 0
                            filters_selected["translator"] = 0
                            filters_selected["binding"] = 0
                            tabText.text =  tr.connections_filters
                            filters["a911_channel_state"].clear()
                            filters["binding_state"].clear()
                            filters["translator_channel_state"].clear()
                            update_filter()
                        }
                    }
                }

                Custom.FontText {
                    id: total_filtered
                    text: tr.filter_result + ": " + total_counter
                    color: ui.colors.white
                    font.pixelSize: 14
                    anchors {
                        verticalCenter: parent.verticalCenter
                        right: parent.right
                    }
                }
            }
        }
    }
    Connections {
        target: app.company_module

        onTotalCounter: {
            total_counter = result
            total_filtered.text = tr.filter_result + ": " + total_counter
        }
    }
}