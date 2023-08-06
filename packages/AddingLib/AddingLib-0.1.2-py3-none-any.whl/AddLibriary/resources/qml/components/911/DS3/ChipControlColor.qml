import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

Row {
    id: chipControlColor

//  If selected first chip
    property int currentIndex: 0
//  To get current color outside the chip
    property var currentColor: colorModel[0].serverColor
//  Colors model with text, circleColor and serverColor
    property var colorModel: [
        {
            text: tr.black,
            circleColor: ui.ds3.special.black,
            serverColor: "BLACK",
        },
        {
            text: tr.white,
            circleColor: ui.ds3.special.white,
            serverColor: "WHITE",
        }
    ]

    height: 64

    spacing: 8

    Repeater {
        id: colorRepeater

        anchors.centerIn: parent

        model: colorModel
        delegate: DS3.ChipColor {
            circleColor: modelData.circleColor
            mainText: modelData.text
            isSelected: chipControlColor.currentIndex == index
            onSelected: () => {
                chipControlColor.currentIndex = index
                chipControlColor.currentColor = modelData.serverColor
            }
        }
    }
}
