import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


AjaxPopup {
    id: popup

    property var filters: appCompany.bindings_model.filters
    property var counters: appCompany.bindings_model.counters

    width: Math.max(row911.width, rowTranslator.width, rowInstallersItem.width) + 64
    height: filterChips.height + 128

    anchors.centerIn: null

    objectName: "bindingsFilterPopup"
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    focus: true
    modal: true
    parent: ApplicationWindow.contentItem
    x: 356
    y: 172
    background: Item {}
    contentItem: Rectangle {
        anchors.fill: parent

        color: ui.ds3.bg.high
        radius: 12

        Column {
            id: filterChips

            width: parent.width

            anchors {
                top: parent.top
                topMargin: 32
            }

            spacing: 24

            Item {
                id: row911Item

                width: parent.width - 64
                height: 56 + 32

                anchors {
                    horizontalCenter: parent.horizontalCenter
                }

                DS3.Text {
                    anchors {
                        top: parent.top
                        left: parent.left
                    }

                    style: ui.ds3.text.body.MRegular
                    text: tr.a911_binding_status
                    color: ui.ds3.figure.secondary
                }
                Column {
                    id: row911

                    height: 32 * 2

                    anchors {
                        left: parent.left
                        bottom: parent.bottom
                    }

                    spacing: 8

                    Row {
                        height: 32

                        spacing: 16

                        DS3.NavigationChip {
                            label: tr.a911_all + " · " + (
                                    counters["pro_desktop_status_filter_counter"]["active"]+
                                    counters["pro_desktop_status_filter_counter"]["no_monitoring"]+
                                    counters["pro_desktop_status_filter_counter"]["in_sleep_mode"]+
                                    counters["pro_desktop_status_filter_counter"]["no_object"]+
                                    counters["pro_desktop_status_filter_counter"]["waiting_for_approval"]+
                                    counters["pro_desktop_status_filter_counter"]["waiting_for_removal"]
                                )
                            selected: filters["pro_desktop_status_filter"].includes("ALL") || filters["pro_desktop_status_filter"].length == 0

                            onClicked: {
                                appCompany.bindings_model.update_filters({"section": "pro_desktop_status_filter", "filter": "ALL"})
                            }
                        }

                        DS3.NavigationChip {
                            label: tr.no_object_911 + " · " + counters["pro_desktop_status_filter_counter"]["no_object"]
                            selected: filters["pro_desktop_status_filter"].includes("NO_OBJECT")

                            onClicked: {
                                appCompany.bindings_model.update_filters({"section": "pro_desktop_status_filter", "filter": "NO_OBJECT"})
                            }
                        }

                        DS3.NavigationChip {
                            label: tr.active_objects_911 + " · " + counters["pro_desktop_status_filter_counter"]["active"]
                            selected: filters["pro_desktop_status_filter"].includes("ACTIVE")

                            onClicked: {
                                appCompany.bindings_model.update_filters({"section": "pro_desktop_status_filter", "filter": "ACTIVE"})
                            }
                        }

                        DS3.NavigationChip {
                            label: tr.no_monitoring_911_hubs + " · " + counters["pro_desktop_status_filter_counter"]["no_monitoring"]
                            selected: filters["pro_desktop_status_filter"].includes("NO_MONITORING")

                            onClicked: {
                                appCompany.bindings_model.update_filters({"section": "pro_desktop_status_filter", "filter": "NO_MONITORING"})
                            }
                        }
                    }
                    Row {
                        height: 32

                        spacing: 16

                        DS3.NavigationChip {
                            label: tr.sleep_mode_objects_911 + " · " + counters["pro_desktop_status_filter_counter"]["in_sleep_mode"]
                            selected: filters["pro_desktop_status_filter"].includes("IN_SLEEP_MODE")

                            onClicked: {
                                appCompany.bindings_model.update_filters({"section": "pro_desktop_status_filter", "filter": "IN_SLEEP_MODE"})
                            }
                        }

                        DS3.NavigationChip {
                            label: tr.monitoring_requested + " · " + counters["pro_desktop_status_filter_counter"]["waiting_for_approval"]
                            selected: filters["pro_desktop_status_filter"].includes("WAITING_FOR_APPROVAL")

                            onClicked: {
                                appCompany.bindings_model.update_filters({"section": "pro_desktop_status_filter", "filter": "WAITING_FOR_APPROVAL"})
                            }
                        }

                        DS3.NavigationChip {
                            label: tr.binding_status_pending_deletion_plural + " · " + counters["pro_desktop_status_filter_counter"]["waiting_for_removal"]
                            selected: filters["pro_desktop_status_filter"].includes("WAITING_FOR_REMOVAL")

                            onClicked: {
                                appCompany.bindings_model.update_filters({"section": "pro_desktop_status_filter", "filter": "WAITING_FOR_REMOVAL"})
                            }
                        }
                    }
                }
            }
            Item {
                id: installersItem

                width: parent.width - 64
                height: visible ? 56 : 0

                anchors {
                    horizontalCenter: parent.horizontalCenter
                }

                visible: appCompany.data.provided_services.installation

                DS3.Text {
                    anchors {
                        top: parent.top
                        left: parent.left
                    }

                    style: ui.ds3.text.body.MRegular
                    text: tr.installation_services_911
                    color: ui.ds3.figure.secondary
                }
                Row {
                    id: rowInstallersItem

                    height: 32
                    spacing: 16

                    anchors {
                        left: parent.left
                        bottom: parent.bottom
                    }

                    DS3.NavigationChip {
                        label: tr.a911_all + " · " + ((counters["installation_status_filter_counter"]["not_provided"] || 0) + counters["installation_status_filter_counter"]["active"] || 0)
                        selected: filters["installation_status_filter"].includes("ALL") || filters["installation_status_filter"].length == 0

                        onClicked: {
                            appCompany.bindings_model.update_filters({"section": "installation_status_filter", "filter": "ALL"})
                        }
                    }

                    DS3.NavigationChip {
                        label: tr.without_installers_filter + " · " + counters["installation_status_filter_counter"]["not_provided"]
                        selected: filters["installation_status_filter"].includes("NOT_PROVIDED")

                        onClicked: {
                            appCompany.bindings_model.update_filters({"section": "installation_status_filter", "filter": "NOT_PROVIDED"})
                        }
                    }

                    DS3.NavigationChip {
                        label: tr.with_installers_filter + " · " + counters["installation_status_filter_counter"]["active"]
                        selected: filters["installation_status_filter"].includes("ACTIVE")

                        onClicked: {
                            appCompany.bindings_model.update_filters({"section": "installation_status_filter", "filter": "ACTIVE"})
                        }
                    }
                }
            }
            Item {
                id: rowTranslatorItem

                width: parent.width - 64
                height: 56

                anchors {
                    horizontalCenter: parent.horizontalCenter
                }

                DS3.Text {
                    anchors {
                        top: parent.top
                        left: parent.left
                    }

                    style: ui.ds3.text.body.MRegular
                    text: tr.translator_binding_status
                    color: ui.ds3.figure.secondary
                }

                Row {
                    id: rowTranslator

                    height: 32
                    spacing: 16

                    anchors {
                        left: parent.left
                        bottom: parent.bottom
                    }

                    DS3.NavigationChip {
                        label: tr.a911_all + " · " + (counters["translator_status_filter_counter"]["no_object"] + counters["translator_status_filter_counter"]["active"])
                        selected: filters["translator_status_filter"].includes("ALL") || filters["translator_status_filter"].length == 0

                        onClicked: {
                            appCompany.bindings_model.update_filters({"section": "translator_status_filter", "filter": "ALL"})
                        }
                    }

                    DS3.NavigationChip {
                        label: tr.no_object_911 + " · " + counters["translator_status_filter_counter"]["no_object"]
                        selected: filters["translator_status_filter"].includes("NO_OBJECT")

                        onClicked: {
                            appCompany.bindings_model.update_filters({"section": "translator_status_filter", "filter": "NO_OBJECT"})
                        }
                    }

                    DS3.NavigationChip {
                        label: tr.active_objects_911 + " · " + counters["translator_status_filter_counter"]["active"]
                        selected: filters["translator_status_filter"].includes("ACTIVE")

                        onClicked: {
                            appCompany.bindings_model.update_filters({"section": "translator_status_filter", "filter": "ACTIVE"})
                        }
                    }
                }
            }
        }

        Rectangle {
            width: parent.width - 64
            height: 1

            anchors {
                bottom: parent.bottom
                bottomMargin: 68
                horizontalCenter: parent.horizontalCenter
            }

            color: ui.colors.white
            opacity: 0.1
        }

        Item {
            width: parent.width / 2 - 32
            height: 20

            anchors {
                left: parent.left
                leftMargin: 32
                bottom: parent.bottom
                bottomMargin: 24
            }

            Custom.HandMouseArea {
                onClicked: {
                    appCompany.bindings_model.clear_filters(true)
                }
            }

            DS3.Text {
                id: resetText
                
                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                text: tr.reset_connections_filter
                style: ui.ds3.text.body.MBold
                color: ui.ds3.figure.interactive
            }
        }

        Item {
            width: parent.width / 2 - 32
            height: 20

            anchors {
                right: parent.right
                rightMargin: 32
                bottom: parent.bottom
                bottomMargin: 24
            }

            DS3.Text {
                id: allText

                anchors {
                    right: parent.right
                    verticalCenter: parent.verticalCenter
                }

                text: tr.filter_result + ": " + appCompany.bindings_model.counter
                style: ui.ds3.text.body.MBold
                color: ui.ds3.figure.contrast
            }
        }

        Custom.BlockLoading {
            minTime: 300
            backgroundRadius: parent.radius
            startSignals: [app.bindings_module.getBindingsCounters]
            stopSignals: [app.bindings_module.getBindingsCountersSuccess, app.bindings_module.getBindingsCountersFailed]
        }
    }

    Component.onCompleted: {
        app.bindings_module.get_hub_company_bindings_counter_batch()
    }

    Connections {
        target: appCompany.bindings_model

        onFiltersChanged: {
            app.bindings_module.get_hub_company_bindings_counter_batch()
        }
    }
}
