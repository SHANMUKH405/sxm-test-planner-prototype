*** Settings ***
Documentation    Deterministic local learning actions.
Library          learning_keywords.py


*** Keywords ***
Play Learning Content
    [Arguments]    ${search}    ${now_playing}
    Set Learning Content    ${search}    ${now_playing}

Switch Learning Source
    [Arguments]    ${source}
    Set Learning Source    ${source}

Learning Source Should Be
    [Arguments]    ${expected}
    ${observed}=    Read Learning Source
    Should Be Equal    ${observed}    ${expected}

Learning Content Should Still Be Playing
    [Arguments]    ${expected}
    ${observed}=    Read Learning Content
    Should Be Equal    ${observed}    ${expected}
