import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    id: settingsSlider

    //  First value
    property var from: 1
    //  Last value
    property var to: 30
    //  Step of the slider
    property var stepSize: 1
    //  Title of the slider
    property alias title: titleItem.title
    //  Current value of the slider
    property alias value: atomSlider.value
    //  AtomSlider component
    property alias atomSlider: atomSlider
    //  Suffix near the values
    property alias suffix: atomSlider.suffix
    //  Thresholds for colors
    property alias colorStops: atomSlider.colorStops
    //  Values of the slider. Calculated automatically
    readonly property var model: [...Array(to - from + 1).keys()].map((x) => x + from).filter(
        (x) => !((x - from) % stepSize)
    )

    width: parent.width
    height: content.height + 24

    color: ui.ds3.bg.highest

    Column {
        id: content

        width: parent.width - 32

        anchors.centerIn: parent

        spacing: 8

        DS3.AtomTitle {
            id: titleItem

            width: parent.width
        }

        DS3.AtomSliderColor {
            id: atomSlider

            width: parent.width

            model: settingsSlider.model
        }
    }
}