import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    id: popup

    Connections {
        target: app

        onActionSuccess: {
            Popups.please_wait_popup()
            app.get_donor_hub_data(migrationNotAvailableHubsList.selected_hub)
        }
    }

    width: 500
    height: 704

    sideMargins: 24

    header: Item {
        height: navBar.height + inputSearch.height

        DS3.NavBarModal {
            id: navBar

            anchors.top: parent.top

            headerText: tr.select_hub_donor

            onClosed: () => {
                popup.close()
            }
        }

        DS3.InputSearch {
            id: inputSearch

            property var inputText: atomInput.text

            onInputTextChanged: {
                filteredAvailableHubsWithoutCurrent.set_search_filter(inputText)
                filteredNotAvailableHubsWithoutCurrent.set_search_filter(inputText)
            }

            Component.onCompleted: {
                filteredAvailableHubsWithoutCurrent.set_search_filter("")
                filteredNotAvailableHubsWithoutCurrent.set_search_filter("")
            }

            width: parent.width

            anchors.bottom: parent.bottom

            placeholder: tr.search_name_id
        }
    }

    DS3.Spacing {
        height: noFilteredHubsContainer.visible ? 48 : 24
    }

    DS3.InfoContainer {
        id: noFilteredHubsContainer

        visible: !filteredAvailableHubsWithoutCurrent.length && !filteredNotAvailableHubsWithoutCurrent.length
        titleComponent.text: tr.no_results_found
        descComponent.text: tr.no_hubs_found_desktop_import
    }

    DS3.TitleSection {
        text: tr.available_hubs_import
        visible: filteredAvailableHubsWithoutCurrent.length
        isCaps: true
        forceTextToLeft: true
        isBgTransparent: true
    }

    DS3.SettingsContainer {
        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        ListView {
            id: migrationAvailableHubsList

            width: parent.width
            height: contentHeight

            spacing: 1
            model: filteredAvailableHubsWithoutCurrent
            interactive: false
            boundsBehavior: Flickable.StopAtBounds

            delegate: DS3.DeviceSelectionSingle {
                id: availableHub

                width: parent.width

                objectName: "delegate"
                atomTitle.title: name
                atomTitle.subtitle: hub_id
                deviceColor: hub_color
                deviceType: {
                    if (hub_type == "YAVIR") {
                        return "yavir_hub"
                    } else if (hub_type == "YAVIR_PLUS" || hub_type == "HUB_FIBRA") {
                        return "fibra_hub"
                    }
                    return "21"
                }

                clickedArea.onClicked: {
                    selectedHub = donor_data
                    popup.close()
                }
            }
        }
    }

    DS3.Spacing {
        height: filteredAvailableHubsWithoutCurrent.length ? 24 : 0
    }

    DS3.TitleSection {
        text: tr.not_available_hubs_import
        visible: filteredNotAvailableHubsWithoutCurrent.length
        isCaps: true
        forceTextToLeft: true
        isBgTransparent: true
    }

    DS3.SettingsContainer {
        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        ListView {
            id: migrationNotAvailableHubsList

            property var selected_hub: null

            width: parent.width
            height: contentHeight

            spacing: 1
            model: filteredNotAvailableHubsWithoutCurrent
            interactive: false
            boundsBehavior: Flickable.StopAtBounds

            delegate: Rectangle {
                width: parent.width
                height: notAvailableHub.height

                DS3.DeviceSelectionSingle {
                    id: notAvailableHub

                    width: parent.width

                    atomTitle.title: name
                    atomTitle.subtitle: hub_id
                    deviceColor: hub_color
                    deviceType: {
                        if (hub_type == "YAVIR") {
                            return "yavir_hub"
                        } else if (hub_type == "YAVIR_PLUS" || hub_type == "HUB_FIBRA") {
                            return "fibra_hub"
                        }
                        return "21"
                    }
                    enabled: false
                }

                DS3.ButtonIcon {
                    id: buttonIcon

                    anchors {
                        right: parent.right
                        rightMargin: 16
                        verticalCenter: parent.verticalCenter
                    }

                    source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"
                    color: ui.ds3.figure.interactive

                    onClicked: {
                        migrationNotAvailableHubsList.selected_hub = donor_data
                        app.check_hub_donor_errors(migrationNotAvailableHubsList.selected_hub)
                    }
                }
            }
        }
    }
}
