import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
//  If alarm is CCO
    property bool isCriticalCOAlarm
    property var fire_alarms: null
    property var actionsEnabled: {
        if (!appUser.company_id || !popup.management) return true
        return companyAccess.HUB_INTERCONNECT_PROCESS && popup.management.facility_access
    }

    width: 500
    height: 700

    title: tr.fire_protect_interconnect_title
    defaultHeaderBackgroundColor: ui.ds3.bg.high

    DS3.Spacing {
        height: 24
    }

    DS3.PlugImageCircle {
        width: parent.width

        icon: isCriticalCOAlarm ? "qrc:/resources/images/Athena/common_icons/COIllustration.svg" : "qrc:/resources/images/Athena/common_icons/FireIllustration.svg"
        iconColor: ui.ds3.figure.base
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Text {
        width: parent.width
        
        text: tr.smoke_interconnect_started
        style: ui.ds3.text.title.SBold
        horizontalAlignment: Text.AlignHCenter
    }

    Repeater {
        id: repeater

        model: fire_alarms

        DS3.Text {
            width: parent.width

            text: util.insert(tr.alt_in_alt, [modelData.name, modelData.room_name])
            style: ui.ds3.text.title.SBold
            horizontalAlignment: Text.AlignHCenter
        }
    }

    DS3.Spacing {
        height: 8
    }

    DS3.Text {
        width: parent.width

        text: `${tr.interconnected_audible_alarm_is_activated}\n${tr.interconnected_audible_alarm_is_activated_with_permissions}`
        style: ui.ds3.text.body.LRegular
        color: ui.ds3.figure.secondary
        horizontalAlignment: Text.AlignHCenter
    }

    footer: DS3.ButtonBar {
        button.text: tr.silence_interconnected_alarms
        button.onClicked: Popups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
            {
                title: tr.are_you_sure_interconnect,
                text: tr.are_you_sure_interconnect_info,
                firstButtonText: tr.interconnect_off_short,
                firstButtonCallback: () => {
                    app.hub_management_module.mute_fire_detectors("ALL_FIRE_DETECTORS_EXCEPT_TRIGGERED")
                    close()
                },
                secondButtonText: tr.cancel,
            }
        )
        buttons: [
            DS3.ButtonOutlined {
                isAttention: true
                text: tr.silence_all_detectors
                buttonIconSource: "qrc:/resources/images/Athena/common_icons/VolumeOff-S.svg"

                onClicked: Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: isCriticalCOAlarm ? tr.interconnect_pop_up_critical_co_title : tr.are_you_sure_interconnect_all,
                        text: isCriticalCOAlarm ? tr.interconnect_pop_up_critical_co_descr : tr.are_you_sure_interconnect_all_info,
                        firstButtonText: isCriticalCOAlarm ? tr.interconnect_pop_up_critical_co_button : tr.interconnect_off_short,
                        firstButtonCallback: () => {
                            app.hub_management_module.mute_fire_detectors("ALL_FIRE_DETECTORS")
                            close()
                        },
                        secondButtonText: tr.cancel,
                    }
                )
            }
        ]
    }
}
