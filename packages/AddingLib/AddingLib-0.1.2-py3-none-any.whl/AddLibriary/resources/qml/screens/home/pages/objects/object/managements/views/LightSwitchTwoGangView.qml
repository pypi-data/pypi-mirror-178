import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as ViewRows
import "qrc:/resources/qml/components/911/DS3" as DS3


LightSwitchView {
    twoGangButton: Item {
        width: parent.width
        height: buttonTitle.height + twoGangButtonContainer.height + 24

        DS3.TitleSection {
            id: buttonTitle

            isCaps: true
            forceTextToLeft: true
            isBgTransparent: true
            text: tr.right_button_lightswitch_title
        }

        DS3.SettingsContainer {
            id: twoGangButtonContainer

            width: parent.width

            anchors.top: buttonTitle.bottom

            ViewRows.ButtonOnOff {
                isOff: !device.channel2_on
                buttonName: device.button2_name
                leftIcon.source: "qrc:/resources/images/Athena/views_icons/LsSecondButton-M.svg"
            }

            ViewRows.OperatingTime {
                visible: !!device.shut_off_mode_enabled_ch2
                duration_time: device.shut_off_period_channel2_str
            }
        }
    }
}