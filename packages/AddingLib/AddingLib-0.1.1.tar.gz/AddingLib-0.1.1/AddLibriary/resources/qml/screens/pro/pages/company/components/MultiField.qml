import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: multiField

    width: parent.width
    height: keyText.contentHeight + listView.contentHeight + distance

    property var key: ""
    property var model: []

    property var maxCount: 0
    property var distance: 0
    property var fieldDistance: 0
    property var maximumLength: 200

    property var useFooter: true
    property var defaultItem: ""
    property var atLeastOneField: false
    property var plusItemVisible: true

    property var validator: null
    property var allFieldsValid: {
        for (var i = 0; i < itemsCollection.length; i++) {
            if (!itemsCollection[i].trim()) return false

            var item = listView.itemAtIndex(i)
            if (item && !item.valid) return false
        }
        return true
    }
    property var multiFieldActive: {
        for (var i = 0; i < itemsCollection.length; i++) {
            var item = listView.itemAtIndex(i)
            if (item && item.control.activeFocus) return true
        }
        return false
    }

    property alias keyText: keyText
    property alias listView: listView

    property var itemsCollection: []

    function addItem() {
        multiField.focus = true
        multiField.listView.model = multiField.listView.model.concat([multiField.defaultItem])
    }

    Desktop.NormalText {
        id: keyText

        text: multiField.key
        color: ui.colors.secondary
        opacity: enabled ? 1 : 0.5
    }

    ListView {
        id: listView

        width: parent.width
        interactive: false
        spacing: fieldDistance

        anchors {
            top: keyText.bottom
            topMargin: model.length > 0 ? fieldDistance : 4
            left: parent.left
            bottom: parent.bottom
        }

        onModelChanged: {
            var items = []
            listView.model.forEach(function(item) {
                items.push(item)
            })
            multiField.itemsCollection = items
        }

        delegate: Custom.TextField {
            id: delegate

            enabled: multiField.enabled
            opacity: enabled ? 1 : 0.5
            width: enabled ? parent.width - 40 : parent.width

            property var valid: control.acceptableInput

            control {
                text: modelData
                rightPadding: deleteImage.visible ? 48 : 8
                maximumLength: multiField.maximumLength
            }

            Image {
                id: deleteImage

                width: 24
                height: 24

                sourceSize {
                    width: 40
                    height: 40
                }

                source: "qrc:/resources/images/icons/control-a-minus-button.svg"
                visible: {
                    if (!multiField.enabled) return false
                    return multiField.atLeastOneField ? listView.model.length > 1 : listView.model.length > 0
                }

                anchors {
                    verticalCenter: delegate.background.verticalCenter
                    right: parent.right
                    rightMargin: 8
                }

                Custom.HandMouseArea {
                    onClicked: {
                        var listViewVar = listView
                        var indexVar = index
                        focus = true
                        listViewVar.model = listViewVar.model.slice(0, indexVar).concat(listViewVar.model.slice(indexVar + 1, listViewVar.model.length))
                    }
                }
            }

            control.onTextChanged: {
                multiField.itemsCollection[index] = control.text.trim()
                multiField.itemsCollectionChanged()
            }

            control.onEditingFinished: {
                listView.model = listView.model.slice(0, index).concat(control.text.trim(), listView.model.slice(index + 1, listView.model.length))
            }

            Component.onCompleted: {
                if (multiField.validator) {
                    control.validator = multiField.validator
                }

                listView.model = listView.model.slice(0, index).concat(control.text.trim(), listView.model.slice(index + 1, listView.model.length))
            }
        }

        footer: Item {
            width: enabled ? parent.width - 40 : parent.width
            height: visible ? 40 + multiField.fieldDistance : 1

            enabled: multiField.enabled
            opacity: enabled ? 1 : 0.5

            visible: {
                if (listView.model.length == 0) return true

                if (!multiField.useFooter) return false
                return multiField.maxCount ? (multiField.maxCount > listView.model.length) && multiField.plusItemVisible : multiField.plusItemVisible
            }

            Rectangle {
                width: parent.width
                height: 40
                radius: height / 2
                color: ui.colors.dark1
                anchors.bottom: parent.bottom

                Image {
                    width: 24
                    height: 24

                    sourceSize {
                        width: 40
                        height: 40
                    }

                    source: "qrc:/resources/images/icons/control-a-plus-button.svg"

                    anchors.centerIn: parent

                    Custom.HandMouseArea {
                        onClicked: {
                            addItem()
                        }
                    }
                }
            }
        }

        Component.onCompleted: {
            if (multiField.model.length == 0) {
                if (multiField.atLeastOneField) {
                    multiField.model = multiField.model.concat([multiField.defaultItem])
                } else {
                    multiField.model = []
                }
            }
            listView.model = multiField.model
        }
    }

    Item {
        id: addItemButton

        width: 40
        height: 40

        visible: {
            if (listView.model.length == 0 || !multiField.enabled || multiField.useFooter) return false
            return multiField.maxCount ? (multiField.maxCount > listView.model.length) && multiField.plusItemVisible : multiField.plusItemVisible
        }

        anchors {
            right: parent.right
            bottom: parent.bottom
            bottomMargin: 5
        }

        Image {
            width: 24
            height: 24

            sourceSize {
                width: 40
                height: 40
            }

            source: "qrc:/resources/images/icons/control-a-plus-button.svg"

            anchors.centerIn: parent

            Custom.HandMouseArea {
                onClicked: {
                    addItem()
                }
            }
        }
    }
}
