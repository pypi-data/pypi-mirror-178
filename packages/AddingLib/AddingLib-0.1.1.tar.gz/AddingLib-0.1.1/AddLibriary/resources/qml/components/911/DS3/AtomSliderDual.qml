import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Column {
    id: atomSliderDual

//  Range slider component
    readonly property alias rangeSlider: control
//  First value
    property int firstValue
//  Second value
    property int secondValue
//  Minimum indices difference between values
    property int minIndexDifference: 1
//  Array of slider values
    property var model: []
//  Suffix
    property var suffix: ""
//  Text of the minimum value
    property string minText
//  Text of the maximum value
    property string maxText

    opacity: enabled ? 1 : 0.3
    layer.enabled: true

    Item {
        id: valueTextsContainer

        width: parent.width
        height: 20

        DS3.Text {
            id: leftValue

            readonly property var position: control.first.handle.x
                + (control.first.handle.width - width) / 2

            anchors {
                left: parent.left
                leftMargin: position > 0 ? Math.min(position, parent.width - width) : 0
            }

            text: `${firstValue}${suffix}`
            style: ui.ds3.text.body.MBold
        }

        DS3.Text {
            id: rightValue

            readonly property var position: control.second.handle.x
                + (control.second.handle.width - width) / 2

            anchors {
                left: parent.left
                leftMargin: position > 0 ? Math.min(position, parent.width - width) : 0
            }

            text: `${secondValue}${suffix}`
            style: ui.ds3.text.body.MBold
        }
    }

    RangeSlider {
        id: control

        readonly property real workingWidth: width - first.handle.width - second.handle.width
        readonly property real interval: workingWidth / (model.length - 1)
        property int firstIndex: model.indexOf(firstValue)
        property int secondIndex: model.indexOf(secondValue)

        width: parent.width
        height: 30

        stepSize: 1
        from: 0
        to: model.length - 1
        padding: 0
        rightPadding: second.handle.width
        snapMode: Slider.SnapAlways

        background: Rectangle {
            y: control.availableHeight / 2 - height / 2

            width: parent.width
            height: 4
            radius: height / 2
            color: ui.ds3.special.hole

            Rectangle {
                x: control.first.handle.x
                width: control.second.handle.x - x
                height: parent.height
                color: ui.ds3.figure.interactive
                radius: height / 2
            }
        }

        first.handle: Rectangle {
            width: 30
            height: width

            x: control.firstIndex * control.interval
            y: control.availableHeight / 2 - height / 2
            radius: width / 2
            color: ui.ds3.special.knob
            border {
                width: 2
                color: ui.ds3.figure.interactive
            }

            Component.onCompleted: x = x

            DS3.MouseArea {
                id: firstHandleArea

                drag {
                    target: parent
                    axis: Drag.XAxis
                    minimumX: 0
                    maximumX: control.second.handle.x - control.second.handle.width
                        - control.interval * minIndexDifference
                    smoothed: false
                }
                onReleased: parent.x = control.firstIndex * control.interval
            }

            onXChanged: {
                control.firstIndex = Math.round((control.first.handle.x) / control.interval)
                atomSliderDual.firstValue = model[control.firstIndex]
            }
        }

        second.handle: Rectangle {
            width: 30
            height: width

            Component.onCompleted: x = x

            x: control.secondIndex * control.interval + control.first.handle.width
            y: control.availableHeight / 2 - height / 2
            radius: width / 2
            color: ui.ds3.special.knob
            border {
                width: 2
                color: ui.ds3.figure.interactive
            }

            DS3.MouseArea {
                id: secondHandleArea

                drag {
                    target: parent
                    axis: Drag.XAxis
                    minimumX: control.first.handle.x + control.first.handle.width
                        + control.interval * minIndexDifference
                    maximumX: control.width - width
                    smoothed: false
                }

                onReleased: parent.x = control.secondIndex * control.interval + control.first.handle.width
            }

            onXChanged: {
                control.secondIndex = Math.round((control.second.handle.x - width) / control.interval)
                atomSliderDual.secondValue = model[control.secondIndex]
            }
        }
    }

    Item {
        id: minMaxTextsContainer

        width: parent.width
        height: 20

        DS3.Text {
            id: minValue

            anchors.left: parent.left

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            text: minText || model[0]
        }

        DS3.Text {
            id: maxValue

            anchors.right: parent.right

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            text: maxText || model[model.length - 1]
        }
    }
}
