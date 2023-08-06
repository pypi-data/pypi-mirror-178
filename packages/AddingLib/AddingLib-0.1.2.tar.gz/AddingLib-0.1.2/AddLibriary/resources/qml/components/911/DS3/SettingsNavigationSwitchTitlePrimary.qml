import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: settingsNavigationSwitchTitlePrimary

//  Title of the settings
    property alias title: atomTitle.title
//  Subtitle of the settings
    property alias subtitle: atomTitle.subtitle
//  Whether selected or not. Do the thing if `hasSwitch` is true
    property alias checked: switchControl.checked
//  Icon on the left
    property alias icon: iconItem.source
//  Image of the company. Do the thing if `isCompany` is true
    property alias companyImage: companyImageItem.source
//  Name of the company. Do the thing if `isCompany` is true
    property alias companyName: companyImageItem.name
//  Whether the settings represent the company
    property alias isCompany: companyImageItem.visible
//  Callback on switch toggled
    property var onToggleCallback: () => checked = !checked

//  Callback on toggle action
    signal toggle
//  On settings navigation clicked
    signal entered

    width: parent.width
    height: Math.max(atomTitle.height, imageBlock.height) + 24

    color: ui.ds3.bg.highest

    DS3.MouseArea {
        onClicked: parent.entered()
    }

    Row {
        id: imageBlock

        height: visible ? 40 : 0

        anchors {
            left: parent.left
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        visible: iconItem.source != "" || companyImageItem.visible

        DS3.Icon {
            id: iconItem

            visible: source != ""
        }

        DS3.CompanyImage {
            id: companyImageItem

            name: title
            visible: false
        }
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: imageBlock.visible ? imageBlock.right : parent.left
            right: rightBlock.left
            margins: 16
            verticalCenter: parent.verticalCenter
        }
    }

    Row {
        id: rightBlock

        anchors {
            right: parent.right
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        spacing: 16

        Item {
            width: switchControl.width
            height: switchControl.height

            DS3.Switch {
                id: switchControl

                onToggle: () => {
                    settingsNavigationSwitchTitlePrimary.toggle()
                    settingsNavigationSwitchTitlePrimary.onToggleCallback()
                }
            }
        }

        DS3.Icon {
            anchors.verticalCenter: parent.verticalCenter

            source: "qrc:/resources/images/Athena/common_icons/ChevronRight-S.svg"
            opacity: enabled ? 1 : 0.3
        }
    }
}