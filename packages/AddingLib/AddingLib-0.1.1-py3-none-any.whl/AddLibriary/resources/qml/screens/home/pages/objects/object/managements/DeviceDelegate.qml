import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: deviceDelegate

    width: parent.width
    height: loader.height

    color: ui.colors.black

    property var settingsVisible: false
    property alias aliasLoader: loader
    property var currentTab: appUser.company_id ? equipment.currentTab : hubSidebar.currentTab
    property var selectedColor: ui.colors.black

    /* ------------------------------------------------ */
    /* desktop tests */
    property var accessiblePrefix: ""
    /* ------------------------------------------------ */

    Custom.RoundedRect {
        id: roundedRect

        width: parent.width
        height: {
            if (device.class_name == "fake_block") return 72
            if (device.class_name == "vhf_bridge") return 104
            if (["multi_transmitter", "multi_transmitter_fibra"].includes(device.class_name) && currentTab == "DEVICES") return 104
            if ([
                "light_switch", "life_quality", "motion_cam", "motion_cam_outdoor", "camera", "fire_protect",
                "fire_protect_plus", "fire_protect2_base"
            ].includes(device.class_name)) return loader.item.height
            if (device.obj_type == "21"  && management.companies.billing.length) {
                return 72 + management.companies.billing.length * 67 + 16
            }
            return 72
        }
        radius: 10
        color: {
            if (!device) return deviceDelegate.selectedColor
            if ((!["multi_transmitter", "multi_transmitter_fibra"].includes(device.class_name) || device.class_name != "fake_block")) return list.currentIndex == index ? deviceDelegate.selectedColor : ui.colors.dark1
            if (list.currentIndex == index) return deviceDelegate.selectedColor
            return loader.item.hidden ? ui.colors.dark1 : ui.colors.dark3
        }
        topRightCorner: {
            return false

            if (!device) return false
            if (index > 0) {
                var prevDev = devices.list.model.get(index - 1)
                var prevItem = devices.list.itemAtIndex(index - 1)
                if (prevDev && (["multi_transmitter", "multi_transmitter_fibra"].includes(prevDev.class_name) || prevDev.class_name == "fake_block" || prevDev.class_name == "vhf_bridge") && currentTab == "DEVICES" && !prevItem.aliasLoader.item.hidden) {
                    if (!prevItem.aliasLoader.item.mtrDevices) return false
                    if (prevItem.aliasLoader.item.mtrDevices.model.length > 0 && prevItem.aliasLoader.item.mtrDevices.currentIndex == prevItem.aliasLoader.item.mtrDevices.model.length - 1) return true
                    if (prevItem.aliasLoader.item.mtrDevices.model.length > 0) return false
                }
            }
            return (list.currentIndex == index - 1) && (list.currentIndex != -1)
        }

        bottomRightCorner: {
            return false

            if (!device) return false
            if ((["multi_transmitter", "multi_transmitter_fibra"].includes(prevDev.class_name) || prevDev.class_name == "fake_block" || prevDev.class_name == "vhf_bridge") && currentTab == "DEVICES" && !loader.item.hidden) {
                if (loader.item.mtrDevices.currentIndex == 0) return true
                if (loader.item.mtrDevices.model.length > 0) return false
            }
            return (list.currentIndex == index + 1) && (list.currentIndex != -1)
        }

        Custom.HandMouseArea {
            onClicked: {
                devices.resetMtrDevicesIndex()
                list.currentIndex = index
            }
        }
    }

    IconSettings {
        visible: {
            if (device.class_name == "fake_block") return false
            return settingsVisible
        }

        /* ------------------------------------------------ */
        /* desktop tests */
        accessiblePrefix: visible ? deviceDelegate.accessiblePrefix : ""
        /* ------------------------------------------------ */
    }

    Loader {
        id: loader

        width: parent.width
        height: {
            if (!device) return 72
            if (device.class_name == "fake_block") return item.height
            if (device.class_name == "vhf_bridge") return item.height
            if (["multi_transmitter", "multi_transmitter_fibra"].includes(device.class_name) && currentTab == "DEVICES") return item.height
            if ([
                "light_switch", "life_quality", "motion_cam", "motion_cam_outdoor", "camera", "fire_protect",
                "fire_protect_plus", "fire_protect2_base"
            ].includes(device.class_name)) return item.height

            if (device.obj_type == "21" && management.companies.billing.length) {
                return 72 + management.companies.billing.length * 67 + 16
            }
            return 72
        }

        anchors.top: parent.top

        source: device ? device.delegate : ""
    }

    /* ---------------------------------------------------- */
    /* desktop tests */
    Accessible.name: deviceDelegate.accessiblePrefix ? deviceDelegate.accessiblePrefix + "_area" : ""
    Accessible.description: "instance of device delegate (group)"
    Accessible.role: Accessible.Grouping
    /* ---------------------------------------------------- */
}