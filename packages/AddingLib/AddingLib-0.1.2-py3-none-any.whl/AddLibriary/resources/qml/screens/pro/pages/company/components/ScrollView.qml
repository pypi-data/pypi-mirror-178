import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


ScrollView {
    id: scrollView

    clip: true
    width: parent.width

    property alias anim: scrollBarAnim

    anchors {
        top: parent.top
        right: parent.right
        bottom: parent.bottom
    }

    ScrollBar.vertical.policy: {
        if (scrollView.contentHeight > scrollView.height) {
            return ScrollBar.AlwaysOn
        }
        return ScrollBar.AlwaysOff
    }

    PropertyAnimation {
        id: scrollBarAnim

        target: scrollView.ScrollBar.vertical
        to: 0
        duration: 300
        property: "position"
    }
}
