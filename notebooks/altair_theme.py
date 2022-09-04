import altair as alt

BLUE="rgb(106, 172, 250)"
GREEN="rgb(62, 204, 156)"
ORANGE="rgb(255, 163, 31)"
PINK="rgb(255, 109, 135)"
PURPLE="rgb(182, 135, 231)"
GRAY_LIGHT="rgb(230, 230, 230)"
GRAY_REGULAR="rgb(189,189,189)"
GRAY_DARK="rgb(108, 108, 108)"

def custom_theme():
    return {
        'config': {
            'axis': {
                'titleColor': GRAY_DARK,
                'titlePadding': 10,
                'titleAchor': 'end',
                'gridColor': GRAY_LIGHT,
                'gridDash': [5,5],
                'domainColor':GRAY_REGULAR,
                'labelColor': GRAY_REGULAR,
                'labelPadding': 5,
                'tickColor': GRAY_REGULAR,
                'tickSize': 3,
            },
            'axisY': {
                'titleAngle': 0,
                'titleY': -20,
                'titleAlign':'left'
            },
            'legend': {                
                  'orient': "bottom",
                  'labelColor': GRAY_DARK,
                  'titleColor': GRAY_DARK
            },
            "view": {
                "stroke": "transparent",
                "continuousHeight": 300,
                "continuousWidth": 400,
            },
        }
    }


alt.themes.register('altair_theme', custom_theme)
alt.themes.enable('altair_theme')