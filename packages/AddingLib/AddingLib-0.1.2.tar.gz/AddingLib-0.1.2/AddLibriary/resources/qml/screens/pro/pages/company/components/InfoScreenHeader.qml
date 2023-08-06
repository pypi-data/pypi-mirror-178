import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: infoScreenHeader

    width: parent.width
    height: infoIconItem.height + 16 + infoTitleItem.height + 16 + infoSubtitleItem.height + 64 + infoButtonItem.height

    property var icon: ""
    property var title: ""
    property var subtitle: ""

    property var buttonText: ""
    property var buttonAction: null

    property var titleColor: ui.colors.white
    property var subtitleColor: ui.colors.light3

    Item {
        id: infoIconItem

        width: infoIcon.sourceSize.width
        height: infoIcon.sourceSize.height

        anchors {
            top: parent.top
            horizontalCenter: parent.horizontalCenter
        }

        Image {
            id: infoIcon

            source: infoScreenHeader.icon

            anchors.centerIn: parent
        }
    }

    Item {
        id: infoTitleItem

        width: parent.width
        height: infoTitle.contentHeight

        anchors {
            top: infoIconItem.bottom
            topMargin: 16
            horizontalCenter: parent.horizontalCenter
        }

        Desktop.NormalText {
            id: infoTitle

            text: infoScreenHeader.title
            size: 32
            bold: true
            color: infoScreenHeader.titleColor
            horizontalAlignment: Text.AlignHCenter

            anchors.fill: parent
        }
    }

    Item {
        id: infoSubtitleItem

        width: parent.width
        height: infoSubtitle.contentHeight

        anchors {
            top: infoTitleItem.bottom
            topMargin: 16
            horizontalCenter: parent.horizontalCenter
        }

        Desktop.NormalText {
            id: infoSubtitle

            text: infoScreenHeader.subtitle
            size: 16
            color: infoScreenHeader.subtitleColor
            textFormat: Text.RichText
            horizontalAlignment: Text.AlignHCenter
            onLinkActivated: Qt.openUrlExternally(link)

            anchors.fill: parent
        }
    }

    Item {
        id: infoButtonItem

        width: infoButton.textButton.contentWidth + 64
        height: 48

        anchors {
            top: infoSubtitleItem.bottom
            topMargin: 64
            horizontalCenter: parent.horizontalCenter
        }

        Custom.Button {
            id: infoButton

            width: parent.width
            text: infoScreenHeader.buttonText
            textButton.textFormat: Text.PlainText

            anchors.centerIn: parent

            onClicked: {
                if (infoScreenHeader.buttonAction) {
                    infoScreenHeader.buttonAction()
                }
            }
        }
    }
}
