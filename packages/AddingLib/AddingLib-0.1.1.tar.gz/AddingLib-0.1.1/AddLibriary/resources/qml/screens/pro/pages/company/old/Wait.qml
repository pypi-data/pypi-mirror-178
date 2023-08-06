import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13
import QtMultimedia 5.14

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: waitItem
    color: ui.colors.dark4

    property var mode: "waiting"
    property var companyId: ""

    Connections {
        target: app.company_module

        onCompanyStatusChanged: {
            if (status == "ACCEPTED") {
                waitItem.companyId = company_id
                waitItem.mode = "accepted"
            }

            if (status == "REJECTED") {
                waitItem.mode = "rejected"
            }
        }
    }

    Item {
        id: waitModeItem
        visible: waitItem.mode == "waiting"
        anchors.fill: parent

        Image {
            id: logoImageWait
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
            id: upTextWait
            text: tr.a911_company_create_request_created_short
            color: ui.colors.white
            opacity: 1
            width: parent.width
            height: contentHeight
            font.pixelSize: 32
            font.bold: true
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors {
                top: logoImageWait.bottom
                topMargin: parent.height / 12
                horizontalCenter: parent.horizontalCenter
            }
        }

        Custom.FontText {
            id: downTextWait
            text: tr.a911_company_create_request_created
            font.pixelSize: 16
            width: 512
            wrapMode: Text.WordWrap
            color: ui.colors.middle1
            height: contentHeight
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors {
                top: upTextWait.bottom
                topMargin: parent.height / 32
                horizontalCenter: parent.horizontalCenter
            }
        }
    }

    Item {
        id: rejectedModeItem
        visible: waitItem.mode == "rejected"
        anchors.fill: parent

        Image {
            id: logoImageRejected
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
            id: upTextRejected
            text: tr.a911_company_create_request_rejected_short
            color: ui.colors.white
            opacity: 1
            width: parent.width
            height: contentHeight
            font.pixelSize: 32
            font.bold: true
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors {
                top: logoImageRejected.bottom
                topMargin: parent.height / 12
                horizontalCenter: parent.horizontalCenter
            }
        }

        Custom.FontText {
            id: downTextRejected
            text: tr.a911_company_create_request_rejected + " <style>a:link { color: '#5ae4aa'; text-decoration: none; }</style><u><a href='https://support.ajax.systems/" + tr.locale + "/for-users/'>" + tr.support_sercive_link + "</a></u>"
            font.pixelSize: 16
            width: 512
            wrapMode: Text.WordWrap
            color: ui.colors.middle1
            height: contentHeight
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            onLinkActivated: Qt.openUrlExternally(link)
            anchors {
                top: upTextRejected.bottom
                topMargin: parent.height / 32
                horizontalCenter: parent.horizontalCenter
            }
        }

        Item {
            width: 256
            height: 40
            visible: true
            anchors {
                top: downTextRejected.bottom
                topMargin: parent.height / 10
                horizontalCenter: parent.horizontalCenter
            }

            Custom.Button {
                width: parent.width
                text: tr.a911_create_company_after_reject
                transparent: true
                color: ui.colors.green1
                anchors.centerIn: parent

                onClicked: {
                    application.debug("pro -> company -> try again")
                    companyLoader.setSource("qrc:/resources/qml/screens/pro/pages/company/RegCompany.qml")
                }
            }
        }
    }

    Item {
        id: acceptedModeItem
        visible: waitItem.mode == "accepted"
        anchors.fill: parent

        Image {
            id: logoImageAccepted
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
            id: upTextAccepted
            text: tr.a911_company_create_request_approved_short
            color: ui.colors.white
            opacity: 1
            width: parent.width
            height: contentHeight
            font.pixelSize: 32
            font.bold: true
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors {
                top: logoImageAccepted.bottom
                topMargin: parent.height / 12
                horizontalCenter: parent.horizontalCenter
            }
        }

        Custom.FontText {
            id: downTextAccepted
            text: tr.a911_company_create_request_approved
            font.pixelSize: 16
            width: 512
            wrapMode: Text.WordWrap
            color: ui.colors.middle1
            height: contentHeight
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors {
                top: upTextAccepted.bottom
                topMargin: parent.height / 32
                horizontalCenter: parent.horizontalCenter
            }
        }

        Item {
            width: 256
            height: 40
            anchors {
                top: downTextAccepted.bottom
                topMargin: parent.height / 10
                horizontalCenter: parent.horizontalCenter
            }

            Custom.Button {
                width: parent.width
                text: tr.a911_go_to_company
                transparent: false
                color: ui.colors.green1
                anchors.centerIn: parent

                onClicked: {
                    application.debug("pro -> company -> go to the new company")
                    app.login_module.login_into_company(waitItem.companyId, "OWNER")
                }
            }
        }
    }
}
