import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: stepItem

    width: parent.width
    height: stepText.contentHeight

    property var step: 0
    property var count: 0

    anchors {
        top: parent.top
        topMargin: 48
        right: parent.right
        rightMargin: 48
    }

    Desktop.NormalText {
        id: stepText

        text: util.insert(tr.navigation_step_out_of, [stepItem.step, stepItem.count])
        color: ui.colors.light3
        size: 32
        bold: true
        horizontalAlignment: Text.AlignHCenter

        anchors.fill: parent
    }
}
