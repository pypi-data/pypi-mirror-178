import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: bindings
    color: companyStack.color

    Connections {
        target: app.bindings_module

        onCancelChannel911RemovalSuccess: {
            var settings = {}
            settings["hub_id"] = infoBindingsComponent.currentObject && infoBindingsComponent.currentObject.hub_id
                ? infoBindingsComponent.currentObject.hub_id
                : ""

            app.bindings_module.get_hub_company_binding(settings)
        }

        onDeleteHubCompanyBindingSuccess: {
            app.bindings_module.get_hub_company_bindings(true)
        }

        onScheduleChannel911RemovalSuccess: (hub_id) => {
            app.bindings_module.get_hub_company_binding({hub_id: hub_id})
        }

        onRemoveChannel911Success: {
            app.bindings_module.get_hub_company_bindings(true)
        }

        onDisableInstallationServiceSuccess: (hub_id) => {
            app.bindings_module.get_hub_company_bindings(true)
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 8

        Item {
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                id: bindingsLayout
                anchors.fill: parent
                spacing: 0

                Panel {
                    id: panel
                }

                BindingsList {
                    id: bindingsList
                }
            }
        }

        Info {
            id: infoBindingsComponent
        }
    }

    Connections {
        target: app.bindings_module

        onGetBindings: {
            infoBindingsComponent.currentObject = null
        }

        onSearchBinding: {
            infoBindingsComponent.currentObject = null
        }
    }
}
