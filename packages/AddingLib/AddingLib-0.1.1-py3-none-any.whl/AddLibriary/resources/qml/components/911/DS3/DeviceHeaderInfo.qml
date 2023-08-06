import QtQuick 2.12
import QtQuick.Controls 2.13
import "qrc:/resources/qml/components/911/DS3" as DS3

Item {
//  Path for main image
    property var imagePath: ''
//  Set visibility for SettingsButton 
    property bool hasSettingsButton: false
//  Property which allows changed buttonIcon
    property alias buttonIcon: buttonIcon
    
    height: 168
    width: parent.width

    DS3.ButtonIcon {
        id: buttonIcon

        anchors {
            right: parent.right
            top: parent.top
            rightMargin: 12
            topMargin: 12
        }

        source: 'qrc:/resources/images/Athena/common_icons/Settings-M.svg'
        visible: hasSettingsButton 
    }
    
    DS3.Image {
        width: 128
        height: 128

        anchors.centerIn: parent

        source: imagePath
    }
}