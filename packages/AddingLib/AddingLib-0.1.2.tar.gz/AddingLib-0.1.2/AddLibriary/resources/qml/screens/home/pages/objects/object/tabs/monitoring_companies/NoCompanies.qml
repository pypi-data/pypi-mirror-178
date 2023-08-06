import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


Item {
    id: noCompanies

    width: parent.width
    height: parent.height - 100

    Item {
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        Column {
            id: column

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            spacing: 16

            Image {
                id: noMonitoringIcon

                sourceSize.width: 64
                sourceSize.height: 64

                anchors.horizontalCenter: parent.horizontalCenter
                source: "qrc:/resources/images/Athena/common_icons/no-monitoring-xl.svg"
            }

            DS3.Text {
                id: titleText

                anchors.horizontalCenter: parent.horizontalCenter
                style: ui.ds3.text.title.LBold
                text: tr.choose_company_desktop_title

            }

            DS3.Text {
                id: bodyText

                anchors.horizontalCenter: parent.horizontalCenter
                style: ui.ds3.text.body.LRegular
                text: tr.choose_company_desktop_descr
            }
        }

        DS3.ButtonContained {
            width: 175

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: column.bottom
            anchors.topMargin: 48

            enabled: hub.current_user.common_params_access && hub.online
            text: tr.choose_company_button

            onClicked: {
                Popups.device_settings_popup(hub, true)
            }
        }
    }
}