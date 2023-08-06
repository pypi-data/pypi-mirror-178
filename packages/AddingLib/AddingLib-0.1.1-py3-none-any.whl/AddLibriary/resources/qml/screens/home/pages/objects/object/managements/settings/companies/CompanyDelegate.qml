import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsNavigationTitlePrimary {
    isCompany: true
    title: company.name
    companyName: company.name
    companyImage: company.logo_url

    onEntered: {
        companyViewLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/companies/CompanyView.qml", {"currentCompany": company})
    }
}
