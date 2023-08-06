import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Column {
    id: atomSlider

//  Current value of the slider
    property var value: model[control.value]
//  List of possible values
    property var model: []
//  Whether from, to and current value text items are visible
    property alias textVisible: textContainer.visible
//  Suffix near the values
    property var suffix: ""
//  Slider pressed flag
    readonly property alias pressed: control.pressed
//  Text of the minimum value
    property string minText
//  Text of the maximum value
    property string maxText

    onValueChanged: control.value = model.indexOf(value)

    opacity: enabled ? 1 : 0.3
    layer.enabled: true

    Item {
        id: textContainer

        width: parent.width
        height: 20

        DS3.Text {
            id: currentValue

            readonly property var position: control.visualPosition *
                (control.availableWidth - control.handle.width) + (control.handle.width - width) / 2

            anchors {
                left: parent.left
                leftMargin: position > 0 ? Math.min(position, parent.width - width) : 0
            }

            text: `${value}${suffix}`
            style: ui.ds3.text.body.MBold
        }
    }

    Slider {
        id: control

        width: parent.width
        height: 30

        stepSize: 1
        from: 0
        to: model.length - 1
        padding: 0
        snapMode: Slider.NoSnap

        onValueChanged: atomSlider.value = model[value]

        background: Item {
            width: parent.width
            height: 4

            y: control.availableHeight / 2 - height / 2

            Rectangle {
                width: (1 - control.visualPosition) * control.availableWidth
                height: parent.height

                anchors.right: parent.right

                radius: height / 2
                color: ui.ds3.special.hole
            }

            Rectangle {
                id: sliderTile

                width: control.visualPosition * control.availableWidth
                height: parent.height

                color: ui.ds3.figure.interactive
                radius: height / 2
            }
        }

        handle: Rectangle {
            id: controlHandle

            width: 30
            height: width

            x: control.visualPosition * (control.availableWidth - width)
            y: (control.availableHeight - height) / 2
            radius: width / 2
            color: ui.ds3.special.knob
            border {
                width: 2
                color: sliderTile.color
            }
        }
    }

    Item {
        id: minMaxTextContainer

        width: parent.width
        height: 20

        visible: textContainer.visible

        DS3.Text {
            id: fromText

            anchors.left: parent.left

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            text: minText || model[0]
        }

        DS3.Text {
            id: toText

            anchors.right: parent.right

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            text: maxText || model[model.length - 1]
        }
    }
}