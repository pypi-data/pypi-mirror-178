import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
    id: agreement

//  Whether checkbox is visible
    property bool isCheckbox: true
//  Text of agreement
    property alias text: agreementText.text
//  Action of checkbox
    property alias clickedArea: agreementCheckbox.clickedArea
//  Whether checked or not
    property alias checked: agreementCheckbox.checked

    width: parent.width
    height: agreementText.height

    DS3.Select {
        id: agreementCheckbox

        anchors {
            left: parent.left
            margins: 16
        }

        visible: isCheckbox
    }

    DS3.Text {
        id: agreementText

        anchors {
            right: parent.right
            left: isCheckbox ? agreementCheckbox.right : parent.left
            margins: 16
        }

        color: ui.ds3.figure.secondary
    }
}