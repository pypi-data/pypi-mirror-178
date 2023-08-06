import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: bindingsPanel
    color: ui.colors.dark3
    Layout.alignment: Qt.AlignTop | Qt.AlignLeft
    Layout.fillWidth: true
    Layout.minimumHeight: 72 + (errorText.visible ? errorText.height : 0)
    Layout.maximumHeight: Layout.minimumHeight
    Layout.rightMargin: infoBindingsComponent.visible ? 0 : 8

    function action() {
        bindingsPanel.forceActiveFocus()

        var settings = {}
        settings["hub_id"] = searchField.control.text

        appCompany.bindings_model.clear_filters(false)
        app.bindings_module.search_hub_company_binding(settings)
    }

    Connections {
        target: app.bindings_module

        onGetBindings: {
            searchField.control.text = ""
            bindingsPanel.forceActiveFocus()
        }

        onSearchBindingFailed: {
            if (result["1"]) {
                searchField.valid = false
                errorText.text = tr.hub_id_eight_symbols_error
            }

            if (result["not_found"]) {
                searchField.notFound = true
            }
        }
    }

    Item {
        id: searchFieldItem
        width: parent.width * 0.43
        height: 40
        anchors {
            top: parent.top
            right: parent.right
            margins: 16
        }

        Custom.SearchField {
            id: searchField
            clearing: false
            anchors.fill: parent
            action: bindingsPanel.action
            placeHolderText: tr.connection_search_911
            radius: control.activeFocus || !valid ? 0 : 10
            border.width: control.activeFocus || !valid ? 1 : 0
            border.color: valid ? ui.colors.green3 : ui.colors.red3
            control.maximumLength: 8
            control.validator: RegExpValidator { regExp: /[0-9A-Fa-f]+/ }

            property var notFound: false

            control.onTextChanged: {
                searchField.valid = true
                searchField.notFound = false
            }

            control.onActiveFocusChanged: {
                searchField.valid = true
                searchField.notFound = false
            }

            Keys.onEnterPressed: {
                bindingsPanel.action()
            }

            Keys.onReturnPressed: {
                bindingsPanel.action()
            }

            Image {
                width: 28
                height: 28
                source: "qrc:/resources/images/icons/ic-clear.png"
                visible: searchField.control.text != ""
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                    rightMargin: 40
                }

                Custom.HandMouseArea {
                    onClicked: {
                        app.bindings_module.get_hub_company_bindings(true)
                    }
                }
            }

            Custom.FontText {
                id: notFoundText
                width: contentWidth
                text: "—  " + tr.no_results_found
                color: ui.colors.middle3
                visible: searchField.notFound
                font.pixelSize: 12
                font.weight: Font.Light
                wrapMode: Text.NoWrap
                horizontalAlignment: Text.AlignRight
                anchors {
                    right: parent.right
                    rightMargin: Math.max(48, parent.width - searchField.control.contentWidth - notFoundText.width - 24)
                    verticalCenter: parent.verticalCenter
                }
            }
        }
    }

    Item {
        width: searchFieldItem.width
        height: errorText.height

        anchors {
            top: searchFieldItem.bottom
            right: searchFieldItem.right
        }

        Custom.FontText {
            id: errorText
            text: ""
            visible: !searchField.valid
            color: ui.colors.red2
            width: parent.width
            font.pixelSize: 14
            wrapMode: Text.WordWrap
            elide: Text.ElideRight
            textFormat: Text.PlainText
            maximumLineCount: 2
            verticalAlignment: Text.AlignVCenter
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
            }
        }
    }

    Item {
        id: filterTabItem

        width: filterTab.width
        height: 32

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 16
        }

        Custom.HandMouseArea {
            onClicked: {
                Popups.bindings_filter_popup()
            }
        }

        Rectangle {
            id: filterTab
            width: filterTabText.width + 44
            height: parent.height
            radius: height / 2
            color: ui.colors.dark4

            Custom.FontText {
                id: filterTabText
                width: contentWidth
                height: contentHeight
                text: tr.connections_filters
                color: ui.colors.middle1
                font.pixelSize: 14
                verticalAlignment: Text.AlignVCenter
                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                    leftMargin: 12
                }
            }

            Item {
                width: 32
                height: 32
                anchors.right: parent.right

                Custom.Triangle {
                    scale: 0.9
                    rotation: 0
                    anchors.centerIn: parent
                }
            }
        }
    }

    Item {
        id: reloadTabItem
        width: refreshIcon.width + refreshText.width + 4
        height: 32
        anchors {
            left: filterTabItem.right
            leftMargin: 16
            verticalCenter: parent.verticalCenter
        }

        Custom.HandMouseArea {
            onClicked: {
                refreshAnim.start()

                app.bindings_module.get_hub_company_bindings(true)
            }
        }

        Image {
            id: refreshIcon
            sourceSize.width: 16
            sourceSize.height: 16
            source: "qrc:/resources/images/desktop/button_icons/refresh.svg"
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
            }

            RotationAnimator {
                id: refreshAnim
                target: refreshIcon
                from: 0
                to: 360
                duration: 500
            }
        }

        Custom.FontText {
            id: refreshText
            width: contentWidth
            height: contentHeight
            text: tr.Refresh_button_desktop
            color: ui.colors.green1
            font.bold: true
            font.pixelSize: 14
            verticalAlignment: Text.AlignVCenter
            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
            }
        }
    }
}
