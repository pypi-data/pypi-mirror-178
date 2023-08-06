import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsContainerItem {
    property alias source: deviceImage.source
    property alias title: atomTitle.title
    property alias tabs: tabsMultiselect.tabs

    width: parent.width
    height: 114

    color: ui.ds3.bg.highest

    DS3.Image {
        id: deviceImage

        width: 80
        height: 80

        anchors {
            left: parent.left
            leftMargin: 8
            verticalCenter: parent.verticalCenter
        }
    }

    DS3.MouseArea {
        onClicked: {
            if (checkMark.checked) {
                tabsMultiselect.tabs.forEach((item) => {
                    if (item.enabled) item.checked = false
                })
            } else {
                tabsMultiselect.tabs.forEach((item) => {
                    if (item.enabled) item.checked = true
                })
            }
            tabsMultiselect.tabsChanged()
        }
    }

    Column {
        anchors {
            left: deviceImage.right
            leftMargin: 16
            right: checkMark.left
            rightMargin: 8
            verticalCenter: parent.verticalCenter
        }

        spacing: 20

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width
        }

        DS3.TabsMultiselect {
            id: tabsMultiselect
        }
    }

    DS3.SelectMulti {
        id: checkMark

        anchors {
            top: parent.top
            topMargin: 12
            right: parent.right
            rightMargin: 16
        }

        checked: tabsMultiselect.tabs.some((item) => item.checked)
    }
}
