import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InputSingleLine {
// Button name
    property var buttonName: "Switch1"

    atomInput {
        label: tr.button_name_title
        text: buttonName
        maximumLength: 48
    }
}