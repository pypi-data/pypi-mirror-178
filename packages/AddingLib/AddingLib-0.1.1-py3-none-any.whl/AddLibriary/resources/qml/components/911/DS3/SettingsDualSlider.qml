import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: settingsDualSlider

    property alias title: atomTitle.title

    property int from: 0
    property int to: 1
    property int stepSize: 1
    readonly property var model: [...Array(to - from + 1).keys()].map((x) => x + from).filter(
        x => !((x - from) % stepSize)
    )
    property alias firstValue: atomSliderDual.firstValue
    property alias secondValue: atomSliderDual.secondValue
    //  AtomSlider component
    property alias atomSlider: atomSliderDual

    width: parent.width
    height: content.height + 24

    color: ui.ds3.bg.highest

    Column {
        id: content

        width: parent.width - 32

        anchors.centerIn: parent

        spacing: 8

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width
        }

        DS3.AtomSliderDual {
            id: atomSliderDual

            width: parent.width

            model: settingsDualSlider.model
            minIndexDifference: 1
        }
    }
}
