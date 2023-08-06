import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.Popup {
    id: popup
//  Title
    property var headerLabel: null
//  Main text
    property var contentText: null
//  First button text
    property var saveContent: null
//  Callback
    property var todo: null

    width: 500

    sideMargins: 24
    hasCrossButton: false

    footer: Item { height: 0 }

    DS3.InfoContainer {
        anchors.horizontalCenter: parent.horizontalCenter

        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/PD_compliant/PD6662Compliament-XL.svg"
        titleComponent.text: headerLabel
        descComponent.text: contentText
    }

    DS3.Spacing {
        height: 32
    }

    DS3.ButtonContained {
        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        text: saveContent

        onClicked: {
            todo()
            popup.close()
        }
    }

    DS3.Spacing {
        height: 8
    }

    DS3.ButtonText {
        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        text: tr.cancel

        onClicked: {
            popup.close()
        }
    }

    DS3.Spacing {
        height: 24
    }
}