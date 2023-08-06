import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13
import QtMultimedia 5.14

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: createItem
    color: ui.colors.dark4

    Image {
        id: logoImage
        sourceSize.width: 152
        sourceSize.height: 152
        source: "qrc:/resources/images/icons/a-logo-pro.svg"
        anchors {
            top: parent.top
            topMargin: parent.height / 6
            horizontalCenter: parent.horizontalCenter
        }
    }

    Custom.FontText {
        id: upText
        text: tr.a911_create_company_first_step_short
        color: ui.colors.white
        opacity: 1
        width: parent.width
        height: contentHeight
        font.pixelSize: 32
        font.bold: true
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        anchors {
            top: logoImage.bottom
            topMargin: parent.height / 12
            horizontalCenter: parent.horizontalCenter
        }
    }

    Custom.FontText {
        id: downText
        text: tr.a911_create_company_first_step_description
        font.pixelSize: 16
        width: 512
        wrapMode: Text.WordWrap
        color: ui.colors.middle1
        height: contentHeight
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        anchors {
            top: upText.bottom
            topMargin: parent.height / 32
            horizontalCenter: parent.horizontalCenter
        }
    }

    Item {
        width: 256
        height: 40
        anchors {
            top: downText.bottom
            topMargin: parent.height / 10
            horizontalCenter: parent.horizontalCenter
        }

        Custom.Button {
            width: parent.width
            text: tr.a911_create_company
            transparent: false
            color: ui.colors.green1
            anchors.centerIn: parent

            onClicked: {
                application.debug("pro -> company -> start company creation")
                companyLoader.setSource("qrc:/resources/qml/screens/pro/pages/company/RegCompany.qml")
            }
        }
    }
}
