import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


ComboBox {
    id: control
    height: 40
    editable: true
    font.family: roboto.name
    font.pixelSize: 14

    model: []

    signal searchStarted()

    property var selectedInstaller: null

    property var defaultText: ""
    property var blockSearch: false

    property alias textLabel: textLabel
    property alias installersPopup: installersPopup

    onActivated: {
        popup.close()
        if (typeof control.model[index] == "undefined") return

        var inst = control.model[index]
        if (!inst) return

        control.blockSearch = true
        control.selectedInstaller = inst
        textLabel.control.text = inst.first_name + " " + inst.last_name + "  •  " + inst.email
        textLabel.control.cursorPosition = 0
    }

    indicator: Item {}

    background: Item {}

    onSearchStarted: {
        if (control.blockSearch) {
            control.blockSearch = false
            return
        }

        control.selectedInstaller = null
        app.employee_module.search_installers({"search_phrase": textLabel.control.text.trim()})
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
        height: 60

        background: Rectangle {
            id: rect
            color: hovered || index == highlightedIndex ? ui.colors.dark1 : ui.colors.dark2
            width: parent.width
            height: delegate.height
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.black
            anchors.bottom: parent.bottom
        }

        Custom.FontText {
            width: parent.width - 40
            text: modelData ? modelData.first_name + " " + modelData.last_name : ""
            color: ui.colors.light3
            font.pixelSize: 14
            maximumLineCount: 1
            elide: Text.ElideRight
            wrapMode: Text.Wrap
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            anchors {
                top: parent.top
                topMargin: 12
                left: parent.left
                leftMargin: 20
            }
        }

        Custom.FontText {
            width: parent.width - 40
            text: modelData ? modelData.email : ""
            color: ui.colors.middle1
            font.pixelSize: 12
            maximumLineCount: 1
            elide: Text.ElideRight
            wrapMode: Text.Wrap
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            anchors {
                bottom: parent.bottom
                bottomMargin: 12
                left: parent.left
                leftMargin: 20
            }
        }

        Image {
            id: selectedImage
            sourceSize.width: 32
            sourceSize.height: 32
            source: "qrc:/resources/images/icons/connect.svg"

            visible: selectedInstaller ? modelData.employee_id == selectedInstaller.employee_id : false

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
                startSignals: [app.employee_module.searchInstallers]
                stopSignals: [app.employee_module.searchInstallersSuccess, app.employee_module.searchInstallersFailed]
            }
        }
    }

    popup: Popup {
        id: installersPopup
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