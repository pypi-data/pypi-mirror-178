import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: settingsSlider

//  First value
    property var from: 1
//  Last value
    property var to: 30
//  Step of the slider
    property var stepSize: 1
//  Value from which step is doubled
    property var doubleStepSizeFrom
//  Alt doubleStep multiplicator (usually it's still 2)
    property var doubleStepMultiplicator: 2
//  Title of the slider
    property alias title: titleItem.title
//  Padding on the left and right
    property var sidePadding: 16
//  Current value of the slider
    property alias value: atomSlider.value
//  Suffix near the values
    property alias suffix: atomSlider.suffix
//  Values of the slider. Calculated automatically
    property var model: [...Array(to - from + 1).keys()].map((x) => x + from).filter(
        (x) => !(
            doubleStepSizeFrom ? (x < doubleStepSizeFrom ?

                (x - from) % stepSize :
                (x - doubleStepSizeFrom) % (doubleStepMultiplicator * stepSize)) :
            (x - from) % stepSize
        )
    )
//  Slider pressed flag
    readonly property alias pressed: atomSlider.pressed

    width: parent.width
    height: content.height + 24

    color: ui.ds3.bg.highest

    Column {
        id: content

        width: parent.width - 2 * sidePadding

        anchors.centerIn: parent

        DS3.AtomTitle {
            id: titleItem

            width: parent.width

            title: "Title"
        }

        DS3.AtomSlider {
            id: atomSlider

            width: parent.width

            model: settingsSlider.model
        }
    }
}