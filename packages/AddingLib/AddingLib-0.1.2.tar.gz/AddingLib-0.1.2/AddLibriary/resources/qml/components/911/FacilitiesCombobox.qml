import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3/" as DS3


ComboBox {
    id: control
    height: 40
    editable: true
    font.family: roboto.name
    font.pixelSize: 14

    model: []

    signal searchStarted()

    property var selectedFacility: null

    property var defaultText: ""
    property var blockSearch: false

    property alias textLabel: textLabel
    property alias facilitiesPopup: facilitiesPopup

    onActivated: {
        popup.close()
        if (typeof control.model[index] == "undefined") return

        control.blockSearch = true
        var obj = control.model[index]
        control.selectedFacility = obj
        textLabel.control.cursorPosition = 0

        let name = obj.general_info ? obj.general_info.name : ""
        let number = obj.general_info ? obj.general_info.registration_number : ""
        textLabel.control.text = name + "  •  № " + number + "  •  ID " + obj.hub_id
    }

    indicator: Item {}

    background: Item {}

    onSearchStarted: {
        if (control.blockSearch) {
            control.blockSearch = false
            return
        }

        control.selectedFacility = null
        app.facility_module.search_installer_facilities({"search_phrase": textLabel.control.text.trim()})
    }

    Timer {
        id: searchTimer
        interval: 200
        running: false

        onTriggered: {
            searchStarted()
        }
    }

    delegate: ItemDelegate {
        id: delegate
        width: control.width
        height: delegateContent.height + 12

        background: Rectangle {
            id: rect
            color: hovered || index == highlightedIndex ? ui.ds3.bg.high : ui.ds3.bg.highest
            width: parent.width
            height: delegate.height
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.black
            anchors.bottom: parent.bottom
        }

        Column {
            id: delegateContent

            width: parent.width - 40

            anchors.centerIn: parent

            DS3.Text {
                width: parent.width

                text: modelData && modelData.general_info ? modelData.general_info.name : ""
            }

            DS3.Text {
                width: parent.width

                text: "№ " + (modelData && modelData.general_info ? modelData.general_info.registration_number : "")
                color: ui.ds3.figure.secondary
            }

            DS3.Text {
                width: parent.width

                text: "ID " + (modelData ? modelData.hub_id : "")
                color: ui.ds3.figure.secondary
            }
        }

        Image {
            id: selectedImage
            sourceSize.width: 32
            sourceSize.height: 32
            source: "qrc:/resources/images/icons/connect.svg"

            visible: selectedFacility ? modelData.facility_id == selectedFacility.facility_id : false

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: 8
            }
        }
    }

    contentItem: Custom.TextField {
        id: textLabel
        width: control.width
        control.text: ""
        control.maximumLength: 300
        placeHolderText: control.defaultText
        anchors {
            top: parent.top
            topMargin: 4
        }

        Connections {
            target: textLabel.control

            onActiveFocusChanged: {
                if (textLabel.control.activeFocus) {
                    popup.open()
                } else {
                    popup.close()
                }
            }

            onTextChanged: {
                searchTimer.stop()
                searchTimer.start()
            }
        }

        Item {
            width: height
            height: parent.height

            anchors {
                left: parent.right
                verticalCenter: parent.verticalCenter
                verticalCenterOffset: -4
            }

            Custom.BlockLoading {
                id: searchLoader
                radius: 8
                minTime: 300
                customOpacity: 0
                startSignals: [app.facility_module.searchInstallerFacilities]
                stopSignals: [app.facility_module.searchInstallerFacilitiesSuccess, app.facility_module.searchInstallerFacilitiesFailed]
            }
        }
    }

    popup: Popup {
        id: facilitiesPopup
        y: control.height + 1
        width: control.width
        height: listView.contentHeight > 360 ? 360 : listView.contentHeight + 21
        padding: 0

        onClosed: {
            textLabel.control.focus = false
        }

        contentItem: ListView {
            id: listView
            height: parent.height - 21
            clip: true
            spacing: 0
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
            boundsBehavior: Flickable.StopAtBounds
            anchors {
                top: parent.top
                topMargin: 8
                bottom: parent.bottom
                bottomMargin: 13
            }

            ScrollBar.vertical: Custom.ScrollBar {
                id: scrollBar
                parent: listView
                anchors {
                    top: parent.top
                    right: parent.right
                    bottom: parent.bottom
                }

                policy: {
                    if (listView.contentHeight > listView.height) {
                        return ScrollBar.AlwaysOn
                    }
                    return ScrollBar.AlwaysOff
                }
            }
        }

        background: Rectangle {
            anchors.fill: parent
            color: ui.colors.dark2
            border.color: "transparent"
            radius: 8
        }
    }
}