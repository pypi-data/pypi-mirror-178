import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
    id: popup

//  List of parsed errors from server
    property var errors
//  Map to get appropriate error description
    readonly property var messageTemplatesDescriptionsMap: ({
        "systems.ajax.a911.error.company.updateProvidedServices.employeeWithMonitoringRoleExists": tr.cannot_delete_monitoring_employees_desktop_descr,
        "systems.ajax.a911.error.company.updateProvidedServices.hubOnMonitoringExists": tr.cannot_delete_monitoring_objects_desktop_descr,
        "systems.ajax.a911.error.company.updateProvidedServices.translatorAccountExists": util.hyperlink(tr.cannot_delete_monitoring_translator_desktop_descr, "mailto:support@ajax.systems"),
        "systems.ajax.a911.error.company.updateProvidedServices.employeeWithInstallationRoleExists": tr.cannot_delete_monitoring_employees_desktop_descr,
        "systems.ajax.a911.error.company.updateProvidedServices.hubOnInstallationExists": tr.cannot_delete_monitoring_objects_desktop_descr,
    })

    width: 500

//    headerItem.backgroundColor: ui.ds3.bg.high

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        width: parent.width

        titleComponent {
            text: tr.cannot_apply_settings_desktop_title
        }
        descComponent {
            text: tr.cannot_apply_settings_desktop_descr
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        Repeater {
            model: popup.errors

            DS3.CommentImportant {
                imageItem.visible: false
                atomTitle {
                    title: modelData.localised_message
                    subtitle: messageTemplatesDescriptionsMap[modelData.message_template]
                }
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    footer: DS3.ButtonBar {
        buttonText: tr.i_will_check

        button.onClicked: popup.close()
    }
}
