import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import 'qrc:/resources/qml/components/911/' as Custom
import 'qrc:/resources/qml/components/911/DS3' as DS3


Rectangle {
    id: bindingsListTopLevel

    property var ownCurrentIndex: -1

    color: companyStack.color
    Layout.alignment: Qt.AlignBottom | Qt.AlignLeft
    Layout.rightMargin: infoBindingsComponent.visible ? 0 : 8
    Layout.minimumHeight: bindingsLayout.height - panel.height - 1
    Layout.maximumHeight: Layout.minimumHeight
    Layout.fillHeight: true
    Layout.fillWidth: true

    function reloadStaticComponent() {
        if (ownCurrentIndex >= 0) infoBindingsComponent.currentObject = bindingsTable.list.model.data(
            bindingsTable.list.model.index(ownCurrentIndex, 0),
            Qt.UserRole + 1
        )
    }

    Custom.BlockLoading {
        startSignals: [app.bindings_module.getBindings, app.bindings_module.getBinding, app.bindings_module.searchBinding]
        stopSignals: [app.bindings_module.getBindingsSuccess, app.bindings_module.getBindingsFailed, app.bindings_module.getBindingSuccess, app.bindings_module.getBindingFailed, app.bindings_module.searchBindingSuccess, app.bindings_module.searchBindingFailed]
        
        minTime: 300
        customOpacity: 0.5
    }

    Connections {
        target: infoBindingsComponent

        onCurrentObjectChanged: {
            if (!infoBindingsComponent.currentObject) ownCurrentIndex = -1
        }
    }

    Connections {
        target: app.bindings_module

        onGetBindingSuccess: reloadStaticComponent()
    }

    DS3.TableView {
        id: bindingsTable

        anchors.fill: parent

        columnNames: {
            let names = [tr.a911_hub_id, tr.object_name, tr.account_number]
            if (appCompany.data.provided_services.monitoring) names.push(tr.a911_binding_status)
            if (appCompany.data.provided_services.installation) names.push(tr.installation_services_911)
            return names
        }
        fractions: [1.5, 5, 2, 3, 3]

        list {
            model: appCompany.filtered_bindings_model
            delegate: Rectangle {
                height: 48
                width: bindingsTable.tableContentWidth

                color: bindingsListTopLevel.ownCurrentIndex == index ? ui.ds3.bg.lowest : ui.ds3.bg.highest

                Row {
                    height: parent.height

                    Item {
                        width: bindingsTable.columnWidths[0]
                        height: parent.height

                        DS3.Text {
                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: parent.left
                                leftMargin: 16
                                right: parent.right
                            }

                            text: binding && binding.hub_id ? binding.hub_id : ui.empty
                            hasElide: true
                        }
                    }

                    Item {
                        width: bindingsTable.columnWidths[1]
                        height: parent.height

                        DS3.Text {
                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: parent.left
                                leftMargin: 8
                                right: parent.right
                            }

                            text: binding && binding.a911_channel_info && binding.a911_channel_info.name
                                ? binding.a911_channel_info.name
                                : ui.empty
                            hasElide: true
                        }
                    }

                    Item {
                        width: bindingsTable.columnWidths[2]
                        height: parent.height

                        DS3.Text {
                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: parent.left
                                leftMargin: 8
                                right: parent.right
                            }

                            text: binding && binding.a911_channel_info && binding.a911_channel_info.registration_number
                                ? binding.a911_channel_info.registration_number
                                : ui.empty
                            hasElide: true
                        }
                    }

                    Item {
                        id: monitoringStatusCell

                        // State of monitoring service
                        property var state: binding
                            ? binding.pro_desktop_status_preview.pro_desktop_status
                            : "NO_OBJECT"

                        width: bindingsTable.columnWidths[3]
                        height: parent.height

                        visible: appCompany.data.provided_services.monitoring

                        DS3.Icon {
                            id: monitoringStatusIcon

                            source: ({
                                ACTIVE:'qrc:/resources/images/icons/binding-active.svg',
                                NO_MONITORING:'qrc:/resources/images/icons/binding-no-monitoring.svg',
                                IN_SLEEP_MODE:'qrc:/resources/images/icons/binding-sleep.svg',
                                NO_OBJECT:'qrc:/resources/images/icons/binding-no-object.svg',
                                WAITING_FOR_APPROVAL:'qrc:/resources/images/icons/binding-pending-approval.svg',
                                WAITING_FOR_REMOVAL:'qrc:/resources/images/icons/binding-pending-delete.svg',
                            }[monitoringStatusCell.state]) || 'qrc:/resources/images/icons/binding-no-monitoring.svg'

                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: parent.left
                                leftMargin: 8
                            }
                        }

                        DS3.Text {
                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: monitoringStatusIcon.right
                                leftMargin: 4
                                right: parent.right
                            }

                            text: ({
                                ACTIVE: tr.on_monitoring,
                                NO_MONITORING: tr.no_monitoring_911_hubs,
                                IN_SLEEP_MODE: tr.sleep_mode_objects_911,
                                NO_OBJECT: tr.no_object_911,
                                WAITING_FOR_APPROVAL: tr.monitoring_requested,
                                WAITING_FOR_REMOVAL: tr.binding_status_pending_deletion,
                            }[monitoringStatusCell.state]) || tr.no_monitoring_911_hubs
                            color: ({
                                ACTIVE: ui.ds3.figure.positiveContrast,
                                NO_MONITORING: ui.ds3.figure.secondary,
                                IN_SLEEP_MODE: ui.ds3.figure.secondary,
                                NO_OBJECT: ui.ds3.figure.secondary,
                                WAITING_FOR_APPROVAL: ui.ds3.figure.secondary,
                                WAITING_FOR_REMOVAL: ui.ds3.figure.attention,
                            }[monitoringStatusCell.state]) || ui.ds3.figure.secondary
                            hasElide: true
                        }
                    }

                    Item {
                        id: installationStatusCell

                        // State of installation service
                        property bool state: !!(binding && binding.installation_service_state
                            && binding.installation_service_state.state == 'ACTIVE')

                        width: bindingsTable.columnWidths[4]
                        height: parent.height

                        visible: appCompany.data.provided_services.installation

                        DS3.Icon {
                            id: installationStatusIcon

                            source: installationStatusCell.state
                                ? 'qrc:/resources/images/icons/Installer-S-active.svg'
                                : 'qrc:/resources/images/icons/Installer-S.svg'

                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: parent.left
                                leftMargin: 8
                            }
                        }

                        DS3.Text {
                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: installationStatusIcon.right
                                leftMargin: 4
                                right: parent.right
                            }

                            text: installationStatusCell.state ? tr.with_installers_filter : tr.without_installers_filter
                            color: installationStatusCell.state ? ui.ds3.figure.positiveContrast : ui.ds3.figure.secondary
                            hasElide: true
                        }
                    }
                }

                DS3.MouseArea {
                    onClicked: {
                        if (bindingsListTopLevel.ownCurrentIndex != index) {
                            bindingsListTopLevel.ownCurrentIndex = index
                            infoBindingsComponent.currentObject = binding
                        } else {
                            bindingsListTopLevel.ownCurrentIndex = -1
                            infoBindingsComponent.currentObject = null
                        }
                    }
                }
            }
        }

        onBottomReached: {
            app.bindings_module.get_hub_company_bindings(false)
        }
    }

    Custom.EmptySpaceLogo {
        visible: bindingsTable.list.model.length == 0
    }
}
