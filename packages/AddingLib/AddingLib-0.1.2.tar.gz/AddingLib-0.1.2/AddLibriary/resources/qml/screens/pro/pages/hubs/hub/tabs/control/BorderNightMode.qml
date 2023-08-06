import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13



Rectangle {
    anchors.fill: parent
    anchors {
        leftMargin: 16
        rightMargin: 16
        topMargin: 16
        bottomMargin: 40
    }
    border {
        color: ui.colors.green2
        width: 1
    }
    color: "transparent"
   Rectangle {
       width: 32
       height: 32
       color: ui.colors.dark3

       anchors {
           bottom: parent.bottom
           bottomMargin: -16
           horizontalCenter: parent.horizontalCenter
       }
       Image {
            source: "qrc:/resources/images/desktop/button_icons/night-mode.svg"
            anchors.centerIn: parent
       }
   }
}