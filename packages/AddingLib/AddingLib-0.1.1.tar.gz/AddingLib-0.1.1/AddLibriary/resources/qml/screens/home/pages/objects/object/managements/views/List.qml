import QtQuick 2.7
import QtQuick.Controls 2.1

ListView {
    id: topLevel

    boundsBehavior: Flickable.StopAtBounds

    /*
    add: Transition {
        NumberAnimation { properties: "scale"; from: 0.8; to: 1.0; duration: 100 }
    }*/

    add: Transition {}

    removeDisplaced: Transition {
        NumberAnimation { properties: "x,y"; duration: 100 }
    }

    clip: true

    spacing: 16

//    ScrollBar.vertical: ScrollBar {
//        id: control
//        policy: {
//            if (topLevel.contentHeight < topLevel.height) {
//                return ScrollBar.AlwaysOff
//            }
//            return ScrollBar.AlwaysOn
//        }
//        anchors.top: topLevel.top
//        anchors.right: topLevel.right
//        anchors.bottom: topLevel.bottom
//
//        contentItem: Rectangle {
//            implicitWidth: 2
//            implicitHeight: 100
//            radius: width / 2
//            color: control.pressed ? "#81e889" : "#9e9e9e"
//            opacity: 0.6
//        }
//
//        background: Rectangle {
//            implicitWidth: 2
//            implicitHeight: 100
//            color: "#575757"
//        }
//    }
}