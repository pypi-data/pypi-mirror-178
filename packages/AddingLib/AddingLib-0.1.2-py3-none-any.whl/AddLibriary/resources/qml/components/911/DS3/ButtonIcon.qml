import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.Icon {
//  For hover manipulation
    property alias buttonIconMouseArea: buttonIconMouseArea
//  On button clicked
    signal clicked

    color: ui.ds3.figure.interactive

    DS3.MouseArea {
        id: buttonIconMouseArea

        onClicked: parent.clicked()
    }
}
