import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


Column {
    width: parent.width

    visible: hub.chimes_available && device.chime_play_available

    DS3.SettingsContainer {
        DS3.SettingsSwitch {
            id: chimesPlaySwitch

            title: tr.chime_play
            enabled: devEnable
            cancelBinding: false
            checked: chimesEnabled
            onSwitched: () => { chimesEnabled = !checked }
        }
    }

    DS3.Comment {
        text: tr.chime_play_info
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        DS3.CommentImportant {
            atomTitle {
                title: tr.chime_activation_settings
                subtitle: tr.chime_activation_siren_info
            }
        }
    }
}