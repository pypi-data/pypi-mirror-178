import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


ComboBox {
    id: control
    height: 40
    font.family: roboto.name
    font.pixelSize: 14

    model: originModel

    property var defaultText: ""
    property alias textLabel: textLabel
    property alias countriesPopup: countriesPopup
    property var currentFieldValue: textLabel.control.text

    property var maxPopupHeight: 360
    property var badgeImageMargin: 0

    property var code: ""
    property var name: ""
    property var includeWorldwide: false
    property var originModel: {
        if (control.includeWorldwide) {
            var worldwide = [{"code": "world", "name": tr.world}]
            return application.countries ? worldwide.concat(application.countries.countries) : worldwide
        }
        return application.countries ? application.countries.countries : []
    }

    function updateName() {
        if (!application.countries) {
            control.name = ""
            return
        }
        control.name = util.get_country_name(control.originModel, control.code)
    }

    onCodeChanged: {
        control.updateName()
    }

    onActivated: {
        popup.close()
        if (typeof control.model[index] == "undefined") return
        control.code = control.model[index]["code"]
    }

    indicator: Item {}

    background: Item {}

    onModelChanged: {
        currentIndex = 0
    }

    delegate: ItemDelegate {
        id: delegate
        width: control.width
        height: 48

        Custom.FontText {
            width: parent.width - 64
            text: modelData.name
            color: ui.colors.white
            font: control.font
            maximumLineCount: 2
            elide: Text.ElideRight
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            anchors {
                left: parent.left
                leftMargin: 12
                verticalCenter: parent.verticalCenter
            }
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.dark4
            anchors.bottom: parent.bottom
        }

        background: Rectangle {
            id: rect
            color: hovered || index == highlightedIndex ? ui.colors.dark2 : ui.colors.dark1
            width: parent.width
            height: delegate.height
        }

        Image {
            id: selectedImage
            visible: textLabel.control.text.toLowerCase() == modelData["name"].toLowerCase()
            sourceSize.width: 40
            sourceSize.height: 40
            source: "qrc:/resources/images/incidents/cards/a-green-badge.svg"

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: control.badgeImageMargin
            }
        }
    }

    contentItem: Custom.TextField {
        id: textLabel
        width: control.width
        control.text: control.name
        control.maximumLength: 100
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
                var temp = util.filter_countries(control.originModel, textLabel.control.text)
                control.model = temp

                if (textLabel.control.text == "" && control.code != "") {
                    control.code = ""
                }
            }
        }
    }

    popup: Popup {
        id: countriesPopup
        y: control.height + 1
        width: control.width
        height: listView.contentHeight > control.maxPopupHeight ? control.maxPopupHeight : listView.contentHeight + 21
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

    Connections {
        target: application

        onCountriesChanged: {
            control.updateName()
        }
    }

    Component.onCompleted: {
        if (control.code) {
            var temp = util.filter_countries(control.originModel, textLabel.control.text)
            control.model = temp
        }
    }
}
