import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/object/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


AjaxPopup {
    id: popup

    width: 320
    height: maxPopupHeight

    objectName: "userPopup"

    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    focus: true
    modal: false

    anchors.centerIn: null
    parent: ApplicationWindow.contentItem

    x: settings.language == "Farsi" ? 0 : parent.width - width
    y: header.height + 64

    signal loadCompanies()
    property var action: null

    property var uiRoles: {
        "OWNER": tr.owner_911,
        "SENIOR_CMS_ENGINEER": tr.a911_Senior_monitoring_station_engineer,
        "CMS_ENGINEER": tr.a911_monitoring_station_engineer,
        "HEAD_OF_INSTALLERS": tr.a911_head_of_installers,
        "INSTALLER": tr.a911_installer,
        "HEAD_OF_OPERATORS": tr.a911_head_of_operators,
        "OPERATOR": tr.a911_operator,
        "RAPID_RESPONSE_TEAM": tr.a911_gbr,
        "PRO": "PRO"
    }

    background: Item {}

    contentItem: Rectangle {
        color: ui.colors.black
        anchors.fill: parent

        Item {
            anchors.fill: parent

            Rectangle {
                id: currentCompany

                width: parent.width - 32
                height: companyItem.height + 16 + titleText.height + 114


                color: ui.colors.black
                radius: 10
                anchors.horizontalCenter: parent.horizontalCenter

                Custom.FontText {
                    id: titleText

                    height: contentHeight

                    text: tr.a911_choose_company
                    elide: Text.ElideRight
                    color: ui.colors.white
                    opacity: 0.5

                    anchors {
                        top: parent.top
                        topMargin: 10
                        left: parent.left
                    }

                    /* ------------------------------------------------ */
                    /* desktop tests */
                    Accessible.name: "account_header_text"
                    Accessible.description: text
                    Accessible.role: Accessible.Paragraph
                    /* ------------------------------------------------ */
                }

                Rectangle {
                    id: privateAccount

                    width: parent.width
                    height: 72

                    color: ui.colors.dark3
                    radius: 10

                    anchors {
                        top: titleText.bottom
                        topMargin: 16
                    }

                    Image {
                        id: proLogo

                        source: "qrc:/resources/images/icons/a-logo-pro.svg"
                        sourceSize {
                            width: 48
                            height: 48
                        }

                        anchors {
                            left: parent.left
                            leftMargin: 9
                            verticalCenter: parent.verticalCenter
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "account_pro_image"
                        Accessible.description: source
                        Accessible.role: Accessible.Graphic
                        /* ------------------------------------------------ */
                    }

                    Custom.FontText {
                        id: privateAccountName

                        text: tr.a911_privat_account

                        width: 172
                        height: parent.height - 24
                        color: ui.colors.light4
                        maximumLineCount: 3
                        wrapMode: Text.Wrap
                        elide: Text.ElideRight
                        textFormat: Text.PlainText
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignLeft

                        anchors {
                            left: proLogo.right
                            leftMargin: 12
                            verticalCenter: parent.verticalCenter
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "account_pro_text"
                        Accessible.description: text
                        Accessible.role: Accessible.Paragraph
                        /* ------------------------------------------------ */
                    }

                    Image {
                        id: badgeImage

                        sourceSize.width: 40
                        sourceSize.height: 40
                        source: {
                            if (!appUser.company_id) return "qrc:/resources/images/icons/a-selected-bage-green.svg"
                            return "qrc:/resources/images/icons/a-unselected-badge.svg"
                        }

                        anchors {
                            right: parent.right
                            rightMargin: 8
                            verticalCenter: parent.verticalCenter
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "account_pro_badge"
                        Accessible.description: !appUser.company_id ? "checked:true" : "checked:false"
                        Accessible.role: Accessible.Graphic
                        /* ------------------------------------------------ */
                    }

                    Custom.HandMouseArea {
                        id: accountProArea

                        enabled: appUser.company_id

                        onClicked: {
                            application.debug("user popup -> change company -> login as PRO")
                            app.login_module.login_into_personal_account()
                        }
                    }

                    /* -------------------------------------------- */
                    /* desktop tests */
                    Accessible.name: "account_pro_area"
                    Accessible.description: "<button enabled=" + Accessible.checkable + ">" + "pro" + "</button>"
                    Accessible.role: Accessible.Button
                    Accessible.checkable: accountProArea.visible && accountProArea.enabled
                    Accessible.onPressAction: {
                        if (!Accessible.checkable) return
                        accountProArea.clicked(true)
                    }
                    /* -------------------------------------------- */
                }

                Rectangle {
                    width: parent.width + 16
                    height: 1

                    color: ui.colors.dark1
                    anchors{
                        top: privateAccount.bottom
                        topMargin: 16
                        left: parent.left
                    }
                }

                Item {
                    width: parent.width
                    height: Math.min(companyItem.contentHeight, companyItem.maxHeight)

                    anchors {
                        top: privateAccount.bottom
                        topMargin: 32
                    }

                    DS3.ScrollView {
                        id: companyItem

                        property var maxHeight: application.height - 470

                        clip: true
                        padding: 0
                        contentSpacing: 8
                        scrollBarHasPadding: false

                        Repeater {
                            id: contentView

                            model: appUser.accepted_companies_wo_personal_account

                            Rectangle {
                                width: parent.width
                                height: 72

                                color: ui.colors.dark3
                                radius: 10

                                Custom.UserImage {
                                    id: companyLogo

                                    width: 42
                                    height: 42

                                    userName: modelData.company_name
                                    imageSource: util.get_image_with_resolution(modelData.company_logo.images, "64x64")

                                    anchors {
                                        left: parent.left
                                        leftMargin: 12
                                        verticalCenter: parent.verticalCenter
                                    }

                                    /* ------------------------------------ */
                                    /* desktop tests */
                                    Accessible.name: __accessible_unique_ids__ ? "account_company_image_" + modelData.company_id : "company_image"
                                    Accessible.description: imageSource ? imageSource : "text:" + userName
                                    Accessible.role: Accessible.Graphic
                                    /* ------------------------------------ */
                                }

                                Custom.FontText {
                                    id: companyName

                                    text:  modelData.company_name

                                    width: 172
                                    height: parent.height - 24

                                    color: ui.colors.light4
                                    maximumLineCount: 3
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    verticalAlignment: Text.AlignVCenter
                                    horizontalAlignment: Text.AlignLeft

                                    anchors {
                                        left: companyLogo.right
                                        leftMargin: 12
                                        verticalCenter: parent.verticalCenter
                                    }

                                    /* ------------------------------------ */
                                    /* desktop tests */
                                    Accessible.name: __accessible_unique_ids__ ? "account_company_text_" + modelData.company_id : "company_text"
                                    Accessible.description: text
                                    Accessible.role: Accessible.Paragraph
                                    /* ------------------------------------ */
                                }

                                Image {
                                    id: badgeImage

                                    sourceSize.width: 40
                                    sourceSize.height: 40
                                    source: {
                                        modelData.company_id == appUser.company_id ?
                                        "qrc:/resources/images/icons/a-selected-bage-green.svg" :
                                        "qrc:/resources/images/icons/a-unselected-badge.svg"
                                    }

                                    anchors {
                                        right: parent.right
                                        rightMargin: 8
                                        verticalCenter: parent.verticalCenter
                                    }

                                    /* ------------------------------------ */
                                    /* desktop tests */
                                    Accessible.name: __accessible_unique_ids__ ? "account_company_badge_" + modelData.company_id : "company_badge"
                                    Accessible.description: modelData.company_id == appUser.company_id ? "checked:true" : "checked:false"
                                    Accessible.role: Accessible.Graphic
                                    /* ------------------------------------ */
                                }

                                Custom.HandMouseArea {
                                    id: accountCompanyArea

                                    enabled: appUser.company_id != modelData.company_id

                                    onClicked: {
                                        if (badgeImage.source != "qrc:/resources/images/icons/a-unselected-badge.svg") return

                                        application.debug("user popup -> change company -> login as " + modelData.role + " into " + modelData.company_id, false)
                                        __ga__.report("activity", "user popup -> change company -> login into COMPANY")
                                        badgeImage.source = "qrc:/resources/images/icons/a-selected-bage-green.svg"
                                        app.login_module.login_into_company(modelData.company_id, modelData.role)
                                    }
                                }

                                /* ------------------------------------ */
                                /* desktop tests */
                                Accessible.name: "account_company_area_" + modelData.company_id
                                Accessible.description: "<button enabled=" + Accessible.checkable + ">" + "company_" + modelData.company_id + "</button>"
                                Accessible.role: Accessible.Button
                                Accessible.checkable: accountCompanyArea.visible && accountCompanyArea.enabled
                                Accessible.onPressAction: {
                                    if (!Accessible.checkable) return
                                    accountCompanyArea.clicked(true)
                                }
                                /* ------------------------------------ */
                            }
                        }
                    }
                }
            }

            Item {
                id: bottomInfo

                anchors.bottom: parent.bottom

                height: 240
                width: parent.width

                Rectangle {
                    width: parent.width - 16
                    height: 1

                    color: ui.colors.dark1
                    anchors{
                        top: parent.top
                        right: parent.right
                    }
                }

                Item {
                    id: userSettings

                    width: parent.width - 32
                    height: 80

                    anchors {
                        top: parent.top
                        topMargin: 16
                        horizontalCenter: parent.horizontalCenter
                    }

                    Rectangle {
                        width: parent.width
                        height: 52

                        radius: 10
                        color: ui.colors.dark3
                        anchors.top: parent.top

                        Custom.FontText {
                            width: parent.width - 64
                            height: parent.height

                            text: tr.a911_profile_settings
                            color: ui.colors.middle1
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            textFormat: Text.PlainText
                            elide: Text.ElideRight
                            anchors {
                                left: parent.left
                                leftMargin: 64
                            }
                        }

                        Image {
                            sourceSize.width: 40
                            sourceSize.height: 40
                            source: "qrc:/resources/images/icons/a-settings-icon.svg"
                            anchors {
                                left: parent.left
                                leftMargin: 12
                                verticalCenter: parent.verticalCenter
                            }
                        }
                        Image {
                            id: rightArrow

                            sourceSize.width: 12
                            sourceSize.height: 21
                            source: "qrc:/resources/images/incidents/cards/a-control-right.svg"
                            anchors {
                                right: parent.right
                                rightMargin: 24
                                verticalCenter: parent.verticalCenter
                            }
                        }
                        ColorOverlay {
                            anchors.fill: rightArrow
                            source: rightArrow
                            color: ui.colors.middle1
                        }
                        Custom.HandMouseArea {
                            onClicked: {
                                application.debug("user popup -> settings popup")
                                addUserSettingsPopup()
                                app.security_module.get_two_fa_state()
                                app.security_module.get_sessions()
                                popup.close()
                            }
                        }
                    }
                }

                Rectangle {
                    width: parent.width - 16
                    height: 1

                    color: ui.colors.dark1
                    anchors{
                        top: userSettings.bottom
                        topMargin: -16
                        right: parent.right
                    }
                }

                Item {
                    id: reportItem

                    width: parent.width
                    height: 24

                    anchors{
                        top: userSettings.bottom
                    }

                    Custom.FontText {
                        width: parent.width - 24
                        height: 24

                        text: tr.report_problem
                        color: ui.colors.light3
                        font.pixelSize: 16
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        anchors {
                            left: parent.left
                            leftMargin: 32
                            verticalCenter: parent.verticalCenter
                        }
                    }

                    Image {
                        sourceSize.width: 20
                        sourceSize.height: 22
                        source: "qrc:/resources/images/icons/problem.svg"
                        anchors {
                            right: parent.right
                            rightMargin: 16
                            verticalCenter: parent.verticalCenter
                        }
                    }

                    Custom.HandMouseArea {
                        onClicked: {
                            application.debug("user popup -> report problem")
                            application.reportPopup({"userName": (appUser.data.user_info.first_name + " " + appUser.data.user_info.last_name), "userEmail": appUser.data.user_info.email})
                            popup.close()
                        }
                    }
                }

                Rectangle {
                    width: parent.width - 16
                    height: 1

                    color: ui.colors.dark1
                    anchors{
                        top: reportItem.bottom
                        topMargin: 16
                        right: parent.right
                    }
                }

                Item {
                    id: exitItem

                    width: parent.width
                    height: 32

                    anchors{
                        top: reportItem.bottom
                        topMargin: 29
                    }

                    Item {
                        width: exitImage.width + 4 + exitText.width
                        height: parent.height
                        anchors {
                            centerIn: parent
                            verticalCenterOffset: 2
                            horizontalCenterOffset: -4
                        }

                        Image {
                            id: exitImage

                            sourceSize.width: 24
                            sourceSize.height: 24
                            source: "qrc:/resources/images/icons/exit.svg"
                            anchors {
                                left: parent.left
                                verticalCenter: parent.verticalCenter
                            }
                        }

                        Custom.FontText {
                            id: exitText

                            width: contentWidth
                            height: 24

                            text: tr.sign_out
                            color: ui.colors.red1
                            font.pixelSize: 16
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            anchors {
                                right: parent.right
                                verticalCenter: parent.verticalCenter
                            }
                        }
                    }

                    Custom.HandMouseArea {
                        id: logoutArea

                        onClicked: {
                            application.debug("user popup -> sign out")
                            app.login_module.logout()
                            screenLoader.source = "qrc:/resources/qml/screens/login/Login.qml"
                        }

                        /* ---------------------------------------- */
                        /* desktop tests */
                        Accessible.name: "account_logout_area"
                        Accessible.description: "<button enabled=" + Accessible.checkable + ">" + "logout" + "</button>"
                        Accessible.role: Accessible.Button
                        Accessible.checkable: visible && enabled
                        Accessible.onPressAction: {
                            if (!Accessible.checkable) return
                            logoutArea.clicked(true)
                        }
                        /* ---------------------------------------- */
                    }
                }

                Item {
                    id: licenseItem

                    width: parent.width - 32
                    height: 16

                    anchors {
                        top: exitItem.bottom
                        topMargin: 16
                        horizontalCenter: parent.horizontalCenter
                    }

                    Custom.FontText {
                        id: licenseText

                        width: parent.width
                        height: contentHeight

                        text: "<a style='text-decoration:underline' href='license'>" + util.colorize(util.insert(tr.ajax_software_license_agreement, ["", "", ""]), ui.colors.middle1) + "</a>"
                        color: ui.colors.middle1
                        font.pixelSize: 14
                        font.underline: true
                        wrapMode: Text.Wrap
                        elide: Text.ElideRight
                        textFormat: Text.RichText
                        maximumLineCount: 1
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignLeft
                        anchors {
                            left: parent.left
                            bottom: parent.bottom
                        }

                        onLinkActivated: {
                            var locale = tr.get_locale()
                            var localeSimplified = () => {
                                if (["ua", "uk"].includes(locale)) { return "ua" }
                                if (["ru", "kz", "by", "localize"].includes(locale)) { return "ru" }
                                return "en"
                            }

                            if (link == "license") {
                                link = "https://ajax.systems/" + localeSimplified() + "/ajax-pro-agreement/"
                                Qt.openUrlExternally(link)
                                return
                            }
                        }
                    }
                }

                Item {
                    id: machineIdItem

                    width: parent.width - 32
                    height: 16

                    anchors {
                        top: exitItem.bottom
                        topMargin: 40
                        horizontalCenter: parent.horizontalCenter
                    }

                    ToolTip {
                        id: tooltip

                        parent: parent
                        contentItem: Text {
                            text: tr.copied
                            font.family: roboto.name
                            font.pixelSize: 12
                            color: ui.colors.light1
                        }

                        background: Rectangle {
                            color: ui.colors.dark1
                            radius: 4
                        }
                    }

                    Custom.HandMouseArea {
                        id: machineIdArea

                        onClicked: {
                            util.set_clipboard_text(appUser && appUser.machine_id ? appUser.machine_id : ui.empty)
                            tooltip.show("", 1000)
                        }
                    }

                    Custom.FontText {
                        id: machineIdText

                        width: parent.width
                        height: contentHeight

                        text: appUser && appUser.machine_id ? tr.machine_id + ": " + appUser.machine_id : tr.machine_id + ": " + ui.empty
                        color: ui.colors.white
                        opacity: machineIdArea.containsMouse ? 0.7 : 0.5
                        font.pixelSize: 14
                        wrapMode: Text.Wrap
                        elide: Text.ElideRight
                        textFormat: Text.PlainText
                        maximumLineCount: 1
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignLeft

                        anchors {
                            left: parent.left
                            bottom: parent.bottom
                        }
                    }
                }
            }
        }

        Loader {
            id: pageLoader

            anchors.fill: parent
            source: ""
        }

        Custom.BlockLoading {
            startSignals: [popup.loadCompanies]
            stopSignals: [appUser.dataReloaded, appUser.dataNotReloaded]
        }
    }

    Connections {
        target: appUser

        onDataReloaded: {
            if (popup.action) popup.action()
        }

        onDataNotReloaded: {
            if (popup.action) popup.action()
        }
    }

    Component.onCompleted: {
        popup.loadCompanies()
        app.get_current_user()
    }

    onClosed: {
        // header.testArea.enabled = true
    }
}