*** Settings ***
Documentation       Local Common Flow learning example using a Test Template.
Resource            ../../resources/sxm_learning.resource
Test Setup           Reset Learning Simulator
Test Template        Switch To The Source And Back In The Learning Simulator
Test Tags            demo    learning    common_flow
Test Timeout         30s


*** Test Cases ***                                  SEARCH                 NOW PLAYING          SOURCE
Learning - SAT-style content - Switch and return    SiriusXM Preview       Ch 1                 FM
    [Tags]    DEMO_SAT_STYLE

Learning - IP-style content - Switch and return     Detroit Red Wings      Detroit Red Wings    FM
    [Tags]    DEMO_IP_STYLE

Learning - Xtra-style content - Switch and return   Women of Rock          Women of Rock         FM
    [Tags]    DEMO_XTRA_STYLE


*** Keywords ***
Switch To The Source And Back In The Learning Simulator
    [Arguments]    ${search}    ${now_playing}    ${source}
    Play Learning Content    ${search}    ${now_playing}
    Switch Learning Source    ${source}
    Learning Source Should Be    ${source}
    Switch Learning Source    SiriusXM
    Learning Source Should Be    SiriusXM
    Learning Content Should Still Be Playing    ${now_playing}
