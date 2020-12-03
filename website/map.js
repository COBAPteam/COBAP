//Fail gracefully
if (!carto.isBrowserSupported()) {
    const reasons = carto.unsupportedBrowserReasons();
    document.getElementById('loader').innerHTML = `
        <div class="open-sans text-white">
          <h3>Oops! Something went wrong.</h3>
          <p>Your browser doesn't support CARTO VL:</p>
          <ul>
              ${reasons.map(r => `<li>${r.message}.</li>`).join('')}
          </ul>
        </div>
      `;
} else {
    const s = carto.expressions;
    const map = new mapboxgl.Map({
        container: 'map',
        //style: carto.basemaps.darkmatter ,
        //Custom map style removing unneeded details 
        style: 'mapstyle.json',
        center: [-20, 30],
        //Disable various controls that aren't useful
        pitchWithRotate: false,
        dragRotate: false,
        touchPitch: false,
        boxZoom: false,
        trackResize: 1,
        customAttribution: "<a href='https://docs.google.com/forms/d/1OGd-56pqT0iRPGv6iJdTnIWWI5vkbF2faAnTz5sDNxI/edit'>Suggest an edit</a>",
        renderWorldCopies: false,
        //Prevent panning past bounds
        maxBounds: new mapboxgl.LngLatBounds(
            new mapboxgl.LngLat(-220, -70),
            new mapboxgl.LngLat(180, 80)),
        minZoom: 2,
        maxZoom: 7,
        zoom: 2
    })
    //Prevent rotation on touch devices
    map.touchZoomRotate.disableRotation();

    //Add zoom controls
    const nav = new mapboxgl.NavigationControl({
        showCompass: false
    });
    map.addControl(nav, 'top-left');

    carto.setDefaultAuth({
        username: 'maryshiraef',
        apiKey: 'default_public'
    })

    popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
    });

    var layerLoaded = 0;
    var displayInfo = 0;
    var animate = 0;
    //const source = new carto.source.GeoJSON(cntrydata)
    days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    months = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    monthformat = { '0': '01', '1': '02', '2': '03', '3': '04', '4': '05', '5': '06', '6': '07', '7': '08', '8': '09', '9': '10', '10': '11' }
    monthdisplay = { '0': 'Jan ', '1': 'Feb ', '2': 'Mar ', '3': 'Apr ', '4': 'May ', '5': 'Jun ', '6': 'Jul ', '7': 'Aug ', '8': 'Sep ', '9': 'Oct ', '10': 'Nov ', '11': 'Dec ' }
    var pipFormats = {}
    var pipDisplay = {}
    var pipValues = []
    var currentMonth = 10;
    var currentday = 29;
    var displaydate = "";
    var formatdate = "";
    var limitWidth = document.body.offsetWidth <= 900;
    var datesforchart = [];
    iso3 = '';
    country = '';
    var countryinfo;
    $.getJSON("countryinfo.json", function (json) {
        countryinfo = json;
    });

    const currentdate = monthformat[currentMonth] + String("0" + currentday).slice(-2)
    var iter = 0
    for (var month of months) {
        if (month > currentMonth) {
            break;
        }
        if (month > 0 & ((limitWidth & month % 2) | !limitWidth))
            pipValues.push(iter);
        for (var day = 1; day <= days[month]; day++) {
            if ((month == currentMonth) & (day > currentday)) {
                break;
            }
            if ((month == 0) & day < 22) {
                continue;
            }
            formatdate = monthformat[month] + String("0" + day).slice(-2);
            pipFormats[iter] = formatdate;
            displaydate = monthdisplay[month] + String("0" + day).slice(-2);
            pipDisplay[iter] = displaydate;
            iter++;
        }
    }
    iter = iter - 1
    if (iter - pipValues[pipValues.length - 1] > 10) {
        pipValues.push(iter);
    }
    slider = noUiSlider.create($(".slider")[0], {
        start: iter,
        step: 1,
        snap: false,
        animate: true,
        orientation: 'horizontal',
        range: {
            'min': [0],
            'max': iter
        },
        tooltips: [{ to: function (a) { return pipDisplay[parseInt(a)]; } }],
        pips: {
            mode: 'values',
            values: pipValues,
            density: 5,
            format: { to: function (a) { return pipDisplay[parseInt(a)]; } }
        }
    });


    for (var month = 1; month <= currentMonth + 1; month++) {
        for (var day = 1; day <= days[month - 1]; day++) {
            if ((month == currentMonth + 1) & (day > currentday)) {
                break;
            }
            if ((month == 1) & day < 22) {
                continue;
            }
            datesforchart.push("2020-" + String(month) + "-" + String(day));
        }
    }

    //Add custom pip for 'WHO declares pandemic'
    document.getElementsByClassName("noUi-value noUi-value-horizontal noUi-value-large")[2].outerHTML += `
        <div id="pandemicNote" class="noUi-value noUi-value-horizontal noUi-value-large" data-value="39" style="left: 20.7447%; transform: translate(0,-250%);width: 262px; color: #ff0000">Mar 11, WHO declares pandemic</div>`


    categories = ["Essentials-only Exception", "Citizen Exception", "Specific Country(ies) Exception", "Workers Exception", "Visa ban(s)", "Citizenship ban(s)", "Travel history ban(s)", "Border Closure(s)", "NONE"];

    tooltipcategories = {
        "Workers Exception": 'A complete closure with exceptions for specific work permit status holders',
        "Specific Country(ies) Exception": 'A complete closure with exceptions for essentials and for nationals from a specific country or listed set of countries (up to 25)',
        "Citizen Exception": 'A complete closure with exceptions for essentials and for citizens (including citizens, permanent residents, and/or the family members of citizens and permanent residents)',
        "Essentials-only Exception": 'A complete closure with exceptions for essentials but not for citizens',
        "Visa ban(s)": 'A partial closure which bans the application for new visas, whether all visa seekers or impacting those from specified countries',
        "Citizenship ban(s)": 'A partial closure which bans foreign nationals from one country or group of countries, e.g. "entry to the country is denied to foreign nationals from Austria, Belgium, and France"',
        "Travel history ban(s)": 'A partial closure which bans travelers who, regardless of nationality, have recently travelled  through or from a specified country or group of countries, e.g. for "All travelers who have been to or travelled through China, Hong Kong, Iran, Italy, and Japan are advised to not enter the country, and may be denied entry"',
        "Border Closure(s)": 'A partial closure which impacts those entering through a specified land, sea or air border; OR all land borders closed OR all air borders closed OR all sea borders closed (but not all three)',
        "NONE": 'No policy recorded at this date'
    };

    colormap = { "Workers Exception": '#a8dbd9', "Specific Country(ies) Exception": '#85c4c9', "Citizen Exception": '#4f90a6', "Essentials-only Exception": '#2a5674', "Visa ban(s)": '#672044', "Citizenship ban(s)": '#ad466c', "Travel history ban(s)": '#e38191', "Border Closure(s)": '#ffc6c4', "NONE": '#888' };
    const colors = ['#a8dbd9', '#85c4c9', '#4f90a6', '#2a5674', '#672044', '#ad466c', '#e38191', '#ffc6c4', '#888'];
    const source = new carto.source.Dataset('cobap1129');
    //Get world borders for background interactivity layer
    const source3 = new carto.source.Dataset('world_borders_hd');
    layer = [];
    viz = [];
    //Use separate columns per policy to allow mutliple policies per country
    let policiesViz2 = `
      @iso3 : $iso3
      @country: $country
      @po0s : 1
      @po1s : 1
      @po2s : 1
      @po0 : ($start_0d <= @selected_d) and ($end_0d > @selected_d) and @po0s
      @po1 : ($start_1d <= @selected_d) and ($end_1d > @selected_d) and @po1s     
      @po2 : ($start_2d <= @selected_d) and ($end_2d > @selected_d) and @po2s
      @selected_d : 246
      @histogram0 : viewportHistogram($policy_0, ['Workers Exception'])
      @histogram1 : viewportHistogram($policy_1, ['Specific Country(ies) Exception'])
      @histogram2 : viewportHistogram($policy_2, ['Citizen Exception'])
      @list: viewportFeatures($policy_0)
      filter: @po0 or @po1 or @po2
      color: blend(#4f90a6,
             blend(#85c4c9,#a8dbd9,@po0),@po0 or @po1)
      strokeColor: rgba(0,0,0,0.2)
      strokeWidth: 1 `
    let policiesViz1 = `
      @country: $country
      @iso3 : $iso3
      @po3s : 1
      @po4s : 1
      @po5s : 1
      @po3 : ($start_3d <= @selected_d) and ($end_3d > @selected_d) and @po3s
      @po4 : ($start_4d <= @selected_d) and ($end_4d > @selected_d) and @po4s
      @po5 : ($start_5d <= @selected_d) and($end_5d > @selected_d) and @po5s
      @histogram3 : viewportHistogram($policy_3, ['Essentials-only Exception'])
      @histogram4 : viewportHistogram($policy_4, ['Visa ban(s)'])
      @histogram5 : viewportHistogram($policy_5, ['Citizenship ban(s)'])
      @selected_d : 246
      color: blend(#ad466c,
             blend(#672044,#2a5674,@po3),@po4 or @po3)
      filter: @po3 or @po4 or @po5 
      strokeColor: rgba(0,0,0,0.2)
      strokeWidth: 1 `

    let policiesViz0 = `
      @country: $country
      @iso3 : $iso3
      @po6s : 1
      @po7s : 1
      @po6 : ($start_6d <= @selected_d) and($end_6d > @selected_d) and @po6s
      @po7 : ($start_7d <= @selected_d) and($end_7d > @selected_d) and @po7s 
      @histogram6 : viewportHistogram($policy_6, ['Travel history ban(s)'])
      @histogram7 : viewportHistogram($policy_7, ['Border Closure(s)']) 
      @selected_d : 246
      color: blend(#ffc6c4,#e38191,@po6)
      filter: @po6 or @po7 
      strokeColor: rgba(0,0,0,0.2)
      strokeWidth: 1 `

    const backgroundViz = `
        @iso3: $adm0_a3
        @country: $admin
        color: #888,
        strokeColor: rgba(0,0,0,0.2)
        strokeWidth: 1 `

    viz[0] = new carto.Viz(backgroundViz);
    viz[1] = new carto.Viz(policiesViz2);
    viz[2] = new carto.Viz(policiesViz1);
    viz[3] = new carto.Viz(policiesViz0);
    layer[0] = new carto.Layer('allcountries', source3, viz[0]);
    layer[1] = new carto.Layer('policies2'   , source , viz[1]);
    layer[2] = new carto.Layer('policies1'   , source , viz[2]);
    layer[3] = new carto.Layer('policies0'   , source , viz[3]);

    layer[0].addTo(map, 'watername_ocean');
    layer[3].addTo(map, 'watername_ocean');
    layer[2].addTo(map, 'watername_ocean');
    layer[1].addTo(map, 'watername_ocean');
    mapwidth = document.getElementById('map').offsetWidth

    //Add onclick for background layer
    const interactivity = new carto.Interactivity(layer[0]);
    interactivity.on('featureClick', updateInfo);

    function drawHistogram() {
        var histogramWidget = document.querySelector('as-category-widget');
        var histogramcombined = [];
        if ($(window).height() > 800) {
            document.querySelector('as-category-widget').style.visibility = 'visible'
            if (layerLoaded == 1) {
                for (i = 0; i < 8; i++) {
                    if (viz[Math.floor(i / 3) + 1].variables['po' + i + 's'].value & viz[Math.floor(i / 3) + 1].variables['histogram' + i].value.length > 0) {
                        if ((viz[Math.floor(i / 3) + 1].variables['histogram' + i].value[0].x == "") & layer[Math.floor(i / 3) + 1].visible & (viz[Math.floor(i / 3) + 1].variables['histogram' + i].value.length > 1))
                            histogramcombined.push(viz[Math.floor(i / 3) + 1].variables['histogram' + i].value[1]);
                        else if (viz[Math.floor(i / 3) + 1].variables['histogram' + i].value[0].x != "")
                            histogramcombined.push(viz[Math.floor(i / 3) + 1].variables['histogram' + i].value[0]);
                    }
                }
                histogramcombined = histogramcombined.sort(function (a, b) { return b.y - a.y })

                histogramWidget.categories = histogramcombined.map(function (entry) {
                    return {
                        name: entry.x,
                        value: entry.y,
                        color: colormap[entry.x]
                    }
                });
            }
        }
        else {
            document.querySelector('as-category-widget').style.visibility = 'hidden'
            document.querySelector('as-category-widget').style.height = '0px'

        }
    }

    carto.on('loaded', layer, () =>  {
        drawHistogram();
        hideSpinner();
        generateLegend();
        setupWidget();
        if (limitWidth)
            minimizelegend();
        layerLoaded = 1;
    });

    carto.on('updated', layer, () => {
        drawHistogram();
    });


    function getCountryByCode(code) {
        return casedata.features.filter(
            function (data) { return data.properties.ISO3 == code }
        );
    }

    const source2 = new carto.source.GeoJSON(casedata);
    let stringViz2a = `
            @date: $5_30_20
            @ddate: $5_30_20d
            @country: $Country
            @iso3: $ISO3
            width: sqrt(@date/600)
            @widthforlegend : globalEqIntervals (@date,7);
            @name: $Country
            color: opacity(#333, .5)
            strokeWidth : 1
            `
    for (var month = 1; month <= currentMonth + 1; month++) {
        for (var day = 1; day <= days[month - 1]; day++) {
            if ((month == currentMonth + 1) & (day > currentday)) {
                break;
            }
            if ((month == 1) & day < 22) {
                continue;
            }
            date = String(month) + "_" + String(day) + "_20";
            stringViz2a = stringViz2a + `
                    @cnt${date} : $${date}
                    `
        }
    }
    for (var month = 1; month <= currentMonth + 1; month++) {
        for (var day = 1; day <= days[month - 1]; day++) {
            if ((month == currentMonth + 1) & (day > currentday)) {
                break;
            }
            if ((month == 1) & day < 22) {
                continue;
            }
            date = String(month) + "_" + String(day) + "_20d";
            stringViz2a = stringViz2a + `
                    @cnt${date} : $${date}
                    `
        }
    }
    const viz2a = new carto.Viz(stringViz2a);

    const layer2a = new carto.Layer('cases', source2, viz2a);
    const interactivity2a = new carto.Interactivity(layer2a);
    const interactivity2aclick = new carto.Interactivity(layer2a);
    if (!iOS()) {
        interactivity2a.on('featureHover', dotName);
        //second interactivity featureclick breaks the first
        //interactivity2aclick.on('featureClick', updateInfo);
    }

    //translate doesn't respect pixel ratio so multiply by pixelratio
    let stringViz3a = `
            @date: $5_30_20d
            @cdate: $5_30_20
            width: sqrt(@date/600)
            @widthforlegend : globalEqIntervals (@date,7);
            @name: $Country
            strokeWidth : 1
            color: opacity(#fff, .5)
            @down: ${window.devicePixelRatio}*sqrt(@cdate/600)/2 - sqrt(@date/600)/2 - 2
            transform: translate(0,-@down)
            `
    for (var month = 1; month <= currentMonth + 1; month++) {
        for (var day = 1; day <= days[month - 1]; day++) {
            if ((month == currentMonth + 1) & (day > currentday)) {
                break;
            }
            if ((month == 1) & day < 22) {
                continue;
            }
            date = String(month) + "_" + String(day) + "_20d";
            stringViz3a = stringViz3a + `
                    @cnt${date} : $${date}
                    `
        }
    }
    for (var month = 1; month <= currentMonth + 1; month++) {
        for (var day = 1; day <= days[month - 1]; day++) {
            if ((month == currentMonth + 1) & (day > currentday)) {
                break;
            }
            if ((month == 1) & day < 22) {
                continue;
            }
            date = String(month) + "_" + String(day) + "_20";
            stringViz3a = stringViz3a + `
                    @cnt${date} : $${date}
                    `
        }
    }
    const viz3a = new carto.Viz(stringViz3a);
    const layer3a = new carto.Layer('deaths', source2, viz3a);

    if (!iOS()) {
        layer2a.addTo(map);
        layer3a.addTo(map);
    }

    function dotName(event) {
        if (event.features.length > 0) {
            const vars = event.features[0].variables;
            cases = numberWithCommas(vars.date.value)
            deaths = numberWithCommas(vars.ddate.value)
            popup.setHTML(`
          <div class="popupinfo">
          <h2 >
          ${vars.name.value}
          </h2>
          <h3 >Confirmed Cases: ${cases}</h3>
          <h3 >Confirmed Deaths: ${deaths}</h3>
          </div>
          `);
            popup.setLngLat([event.coordinates.lng, event.coordinates.lat]);
            if (!popup.isOpen()) {
                popup.addTo(map);
            }
        } else {
            popup.remove();
        }
    }

    function generateLegend() {
        // Request data for legend from the layer viz
        let legendList = `<div class="tooltip"><h4>Complete Closures <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path style="fill:white" d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"/></svg></h4></label>
            <span class="tooltiptext">A new policy in which all newcomers are banned from all ports of entry - AIR, LAND, and SEA - with limited exceptions, including citizens, nationals from a specified country or set of up to 25 countries, and/or essential reasons, e.g. health emergencies, extreme humanitarian/diplomatic reasons, dignitaries, cargo flights, commercial transport, essential deliveries, permanent residents, existing visa holders, and family members of citizens</span></div>`
        for (var i = 0; i <= 7; i++) {
            if (i == 4) {
                legendList += `<div class="tooltip"><h4>Partial Closures <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path style="fill:white" d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"/></svg></h4></label>
            <span class="tooltiptext">A new policy which restricts access of specific groups of people, whether by certain nationalities, travel histories; those entering through a specified land, sea or air border; OR all land borders closed OR all air borders closed OR all sea borders closed (but not all three)</span></div>`
            }
            color = colormap[categories[i]]
            legendList += `<li>
            <label for="js-checkbox-${i}">
            <input
              id="js-checkbox-${i}"
              class="js-checkbox"
              type="checkbox"
              name="categories"
              category="${i}"
            checked>
            <span class="point-mark" style="background-color:${color};"></span>
            <div class="tooltip">` + categories[i] + ` <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path style="fill:white" d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"/></svg></label>
            <span class="tooltiptext">`+ tooltipcategories[categories[i]] + `</span></div>
          </li>\n`
        }
        legendList += `<li>
            <div class="tooltip"><label for="js-checkbox-8">
            <span class="point-mark" style="background-color:#888;"></span>No Data <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path style="fill:white" d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"/></svg></label>
            <span class="tooltiptext">`+ tooltipcategories[categories[8]] + `</span></div>
          </li>\n`
        if (!iOS()) {
            legendList += `<h3>Covid-19 Stats <label for="js-checkbox-stat">
            <input
              id="js-checkbox-stat"
              class="js-checkbox-stat"
              type="checkbox"
              name="categories"
              category="stats"
            checked></label></h3>
      <svg width="300" height="65"><g transform="translate(0, 0)" id="vis"><g class="legend-wrap" transform="translate(-120,-20)"><g class="values-wrap"><circle class="values values-25" r="25" cx="159" cy="55" style="fill: rgb(102, 102, 102); stroke: rgb(255, 255, 255); opacity: 0.5;"></circle><circle class="values values-0.6875" r="4.145780987944249" cx="159" cy="75.85421901205575" style="fill: rgb(255, 255, 255); stroke: rgb(255, 255, 255); opacity: 0.5;"></circle></g><g class="values-line-wrap"><line x1="159" x2="198" y1="30" y2="30" opacity="0.5" style="stroke: rgb(255, 255, 255);"></line><line x1="159" x2="198" y1="71.7084380241115" y2="71.7084380241115" opacity="0.5" style="stroke: rgb(255, 255, 255);"></line></g><g class="values-labels-wrap"><text x="278" y="34" shape-rendering="crispEdges" font-family="'Poppins',Arial" font-size="14" style="text-anchor: end; fill: rgb(200, 200, 200);"><tspan x="314" dy="0em">Confirmed Cases</tspan></text><text x="278" y="75.7084380241115" shape-rendering="crispEdges" font-family="Arial" font-size="14" style="text-anchor: end; fill: rgb(255, 255, 255);"><tspan x="314" dy="0em">Confirmed Deaths</tspan></text></g></g></g></svg>`
        }
        document.getElementById('content').innerHTML = legendList;
    }

    function minimizelegend() {
        document.getElementById('toolbox').style.display = 'none';
        document.getElementById('minilegend').style.display = 'unset';
    }
    function showlegend() {
        document.getElementById('toolbox').style.display = 'unset';
        document.getElementById('minilegend').style.display = 'none';
    }
    function setupWidget() {
        const checkboxes = document.getElementsByClassName('js-checkbox');
        for (let i in checkboxes) {
            const checkbox = checkboxes.item(i);
            checkbox.addEventListener('change', toggleCategory);
        };
        const checkboxstat = document.getElementsByClassName('js-checkbox-stat').item(0);
        if (!iOS()) {
            checkboxstat.addEventListener('change', toggleCases);
        }

    }

    function toggleCategory(event) {
        const checkboxElement = event.currentTarget;
        var cat = checkboxElement.getAttribute('category');
        if (cat < 4) cat = Math.abs(cat - 3)
        if (layer[Math.floor(cat / 3)+1].viz.variables['po' + cat + 's'].value != 0) {
            layer[Math.floor(cat / 3)+1].viz.variables['po' + cat + 's'] = 0;
        }
        else {
            layer[Math.floor(cat / 3)+1].viz.variables['po' + cat + 's'] = 1
        }
        drawHistogram();
    }

    function toggleCases(event) {
        const checkboxElement = event.currentTarget;
        if (layer2a.visible) {
            layer2a.hide();
            layer3a.hide();
        }
        else {
            layer2a.show();
            layer3a.show();
        }
    }
    function rgbToHex(color) {
        return "#" + ((1 << 24) + (color.r << 16) + (color.g << 8) + color.b).toString(16).slice(1);
    }

    //range slider update function
    function debounce(func, wait, immediate) {
        var timeout;
        return function () {
            var context = this, args = arguments;
            var later = function () {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    slider.on('update', debounce(onSlide, 20));

    function onSlide(values, handle) {
        showdate = pipFormats[parseInt(values[0])]
        popup.remove();
        viz[1].variables['selected_d'] = parseInt(values[0]) + 21;
        viz[2].variables['selected_d'] = parseInt(values[0]) + 21;
        viz[3].variables['selected_d'] = parseInt(values[0]) + 21;
        if (pipFormats[parseInt(values[0])].charAt(0) == '0' & pipFormats[parseInt(values[0])].charAt(2) == '0' & !iOS()) {
            viz2a.variables['date'] = viz2a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(3) + "_20"]
            viz2a.variables['ddate'] = viz2a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(3) + "_20d"]
            viz3a.variables['date'] = viz3a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(3) + "_20d"]
            viz3a.variables['cdate'] = viz3a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(3) + "_20"]
        }
        else if (pipFormats[parseInt(values[0])].charAt(0) == '0' & pipFormats[parseInt(values[0])].charAt(2) != '0' & !iOS()){
            viz2a.variables['date'] = viz2a.variables['cnt'  + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(2) + pipFormats[parseInt(values[0])].charAt(3) + "_20"]
            viz2a.variables['ddate'] = viz2a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(2) + pipFormats[parseInt(values[0])].charAt(3) + "_20d"]
            viz3a.variables['date'] = viz3a.variables['cnt'  + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(2) + pipFormats[parseInt(values[0])].charAt(3) + "_20d"]
            viz3a.variables['cdate'] = viz3a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(2) + pipFormats[parseInt(values[0])].charAt(3) + "_20"]
        }        
        else if (pipFormats[parseInt(values[0])].charAt(0) != '0' & pipFormats[parseInt(values[0])].charAt(2) == '0' & !iOS()){
            viz2a.variables['date'] = viz2a.variables['cnt'  + pipFormats[parseInt(values[0])].charAt(0) + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(3) + "_20"]
            viz2a.variables['ddate'] = viz2a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(0) + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(3) + "_20d"]
            viz3a.variables['date'] = viz3a.variables['cnt'  + pipFormats[parseInt(values[0])].charAt(0) + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(3) + "_20d"]
            viz3a.variables['cdate'] = viz3a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(0) + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(3) + "_20"]
        }
        else if (!iOS()){
            viz2a.variables['date'] = viz2a.variables['cnt'  + pipFormats[parseInt(values[0])].charAt(0) + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(2) + pipFormats[parseInt(values[0])].charAt(3) + "_20"]
            viz2a.variables['ddate'] = viz2a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(0) + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(2) + pipFormats[parseInt(values[0])].charAt(3) + "_20d"]
            viz3a.variables['date'] = viz3a.variables['cnt'  + pipFormats[parseInt(values[0])].charAt(0) + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(2) + pipFormats[parseInt(values[0])].charAt(3) + "_20d"]
            viz3a.variables['cdate'] = viz3a.variables['cnt' + pipFormats[parseInt(values[0])].charAt(0) + pipFormats[parseInt(values[0])].charAt(1) + "_" + pipFormats[parseInt(values[0])].charAt(2) + pipFormats[parseInt(values[0])].charAt(3) + "_20"]
        }
        //drawHistogram()
        if ((layerLoaded == 1) & (displayInfo == 1))
            drawinfo(iso3, country, parseInt(values[0]))
    };

    function checkAll() {
        var items = document.getElementsByName('categories');
        for (var i = 0; i < items.length; i++) {
            if (items[i].type == 'checkbox')
                items[i].checked = true;
        }
    }

    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    function hideSpinner() {
        document.getElementById('spinner').innerHTML = '<button onclick="hideLoader()">Go to the Map</button>';
    }
    function hideLoader() {
        document.getElementById('loader').style.opacity = '0';
        document.getElementById('loader').style.pointerEvents = 'none'
    }

    function animateslider() {
        hideInfo();
        if (animate == 1) {
            document.getElementById('animatecontrol').innerHTML = `<path style="fill:white" d="M8 5v14l11-7z"/>`
            animate = 0;
        }
        else {
            animate = 1;
            document.getElementById('animatecontrol').innerHTML = `<path style="fill:white" d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>`
            if (parseInt(slider.get()) == Object.keys(pipDisplay).length - 1)
                slider.set(0)
            setTimeout(animatehandler, 1)
        }
    }

    function pauseslider() {
        animate = 0
        document.getElementById('animatecontrol').onclick = `animateslider()`
    }

    dragElement(document.getElementById("toolbox"));

    var PADDING = 8;
    var rect;
    var viewport = {
        bottom: 0,
        left: 0,
        right: 0,
        top: 0
    }

    window.onresize = function (event) {
        map.resize();
        mapwidth = document.body.offsetWidth
        infoshow = document.getElementById('info').display == "block"
        document.getElementById('map').style.width = mapwidth - (infoshow ? document.getElementById('info').offsetWidth : 0) + 'px'
    };



    function updateInfo(event) {
        if (event.features.length > 0) {
            const vars = event.features[0].variables;
            iso3 = vars.iso3.value;
            country = vars.country.value;
            date = parseInt(slider.get())
            displayInfo = 1;
            drawinfo(iso3, country, date)
        } else {
            hideInfo();
        }
    }


    function drawinfo(iso3, country, date) {

        csvtestarray = readinfo(csvtest, '|');
        currentcountry = []
        showdate = pipFormats[date]

        for (var i = 0; i < csvtestarray.length; i++) {
            if (csvtestarray[i][0] == iso3) {
                currentcountry.push(csvtestarray[i])
            }
        }

        authorityfound = 0;
        dashboardfound = 0;
        if (countryinfo[iso3] != null) {
            if (countryinfo[iso3][0]['3'] != '') {
                site1 = countryinfo[iso3][0]['3'];
                site1link = countryinfo[iso3][0]['4'];
                authorityfound = 1;
                eusite1 = countryinfo['EU'][0]['3'];
                eusite1link = countryinfo['EU'][0]['4'];

            }
            if (countryinfo[iso3][0]['8'] == '1') {
                dashboard = countryinfo[iso3][0]['7'];
                dashboardfound = 1;
                eudashboard = countryinfo['EU'][0]['7'];
            }
        }
        
        eu = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"];
        //console.warn(iso3);
        currentpoliciesc = []
        currentpoliciesp = []

        for (var i = 0; i < currentcountry.length; i++) {
            if (((currentcountry[i][3] < parseInt(showdate.slice(0, 2))) |
                ((currentcountry[i][3] == parseInt(showdate.slice(0, 2))) & (currentcountry[i][4] <= parseInt(showdate.slice(2))))) & currentcountry[i][7] != '' &
                ((currentcountry[i][5] > parseInt(showdate.slice(0, 2))) |
                    ((currentcountry[i][5] == parseInt(showdate.slice(0, 2))) & (currentcountry[i][6] >= parseInt(showdate.slice(2))))) & currentcountry[i][2] != 'NONE' &
                (currentcountry[i][2] == 'Essentials-only Exception' | currentcountry[i][2] == 'Citizen Exception' |
                    currentcountry[i][2] == 'Specific Country(ies) Exception' | currentcountry[i][2] == 'Workers Exception'))

                currentpoliciesc.push(currentcountry[i])
        }
        for (var i = 0; i < currentcountry.length; i++) {
            if (((currentcountry[i][3] < parseInt(showdate.slice(0, 2))) |
                ((currentcountry[i][3] == parseInt(showdate.slice(0, 2))) & (currentcountry[i][4] <= parseInt(showdate.slice(2))))) & currentcountry[i][7] != '' &
                ((currentcountry[i][5] > parseInt(showdate.slice(0, 2))) |
                    ((currentcountry[i][5] == parseInt(showdate.slice(0, 2))) & (currentcountry[i][6] >= parseInt(showdate.slice(2))))) & currentcountry[i][2] != 'NONE' &
                (currentcountry[i][2] == 'Visa ban' | currentcountry[i][2] == 'Citizenship ban' |
                    currentcountry[i][2] == 'Travel history ban' | currentcountry[i][2] == 'Border Closure'))

                currentpoliciesp.push(currentcountry[i])
        }

        currentpoliciesc.sort(function (a, b) {
            return a[4] - b[4]
        });

        currentpoliciesc.sort(function (a, b) {
            return a[3] - b[3]
        });
        currentpoliciesp.sort(function (a, b) {
            return a[4] - b[4]
        });

        currentpoliciesp.sort(function (a, b) {
            return a[3] - b[3]
        });

        infohtml = `
        <div id="subinfo">
          <svg xmlns="http://www.w3.org/2000/svg" onclick="hideInfo()" style="cursor: pointer;position:fixed;top:40px;right:20px;"width="24" height="24" viewBox="0 0 24 24"><path style="stroke: #aaa;fill: #aaa;" d="M14.59 8L12 10.59 9.41 8 8 9.41 10.59 12 8 14.59 9.41 16 12 13.41 14.59 16 16 14.59 13.41 12 16 9.41 14.59 8zM12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>
          <h1 class="CDB-infowindow-title " style="padding-top:20px">
            ${country}<hr>
          </h1>
          
          <div id='policytable'>
          <h2 class="CDB-infowindow-subtitle">Country-Specific Resources:</h2>`
          if(authorityfound)
          infohtml += `Entity responsible for border closures:
          <p><a href='`+ site1link + `'target="_blank" rel="noopener noreferrer">` + site1 +`</a></p>`
        if (eu.includes(iso3))
            infohtml += `<p><a href='` + eusite1link + `'target="_blank" rel="noopener noreferrer">` + eusite1 + `</a></p>`
        if (dashboardfound)
              infohtml += `<p><a href='` + dashboard + `'target="_blank" rel="noopener noreferrer">Covid-19 Dashboard</a></p>`
        if (eu.includes(iso3))
            infohtml += `<p><a href='` + eudashboard + `'target="_blank" rel="noopener noreferrer">European Union Covid-19 Dashboard</a></p>`

        infohtml += `
          <h2 class="CDB-infowindow-subtitle">Policies active on `+ monthdisplay[parseInt(showdate.slice(0, 2)) - 1] + ` ` + showdate.slice(2) + `:</h2>`
        if (currentpoliciesc.length > 0) {
            infohtml += `
            <h3 style="color:white">Complete Closures</h3>
            <table style="width:100%"><tr>
            <th>Policy Type</th>
            <th>Date 
            Implemented</th>
            <th>Date Expires</th>
            <th>Source</th>
            </tr>`
            for (var i = 0; i < currentpoliciesc.length; i++) {
                infohtml += `<tr><th>
            ${currentpoliciesc[i][2]} </th><th> 
            ${currentpoliciesc[i][3]} / ${currentpoliciesc[i][4]} </th><th> `
                if (currentpoliciesc[i][5] == '12' & currentpoliciesc[i][6] == '31')
                    infohtml += `None </th><th> `
                else
                    infohtml += `${currentpoliciesc[i][5]} / ${currentpoliciesc[i][6]} </th><th> `
                if (currentpoliciesc[i][7].includes('web.archive.org')) {
                    url = currentpoliciesc[i][7].split('web.archive.org')[1].split('/')
                    url.shift()
                    url.shift()
                    url.shift()
                    if (url[0].includes('http'))
                        url.shift()
                    url = 'http://' + url.join('/')
                    infohtml += `<a href='${url}' target="_blank" rel="noopener noreferrer" >Source</a><br><a href='${currentpoliciesc[i][7]}' target="_blank" rel="noopener noreferrer" >(Archive)</a> </th></tr>`

                }
                else
                    infohtml += `<a href='${currentpoliciesc[i][7]}' target="_blank" rel="noopener noreferrer" >Source</a> </th></tr>`
            }
        }
        else
            infohtml += '<h3 style="color:white">Complete Closures</h3>&nbsp;&nbsp;&nbsp;No Complete Closures at this date'


        infohtml += `</table></div>`;

        if (currentpoliciesp.length > 0) {
            infohtml += `
            <h3 style="color:white">Partial Closures</h3>
            <table style="width:100%"><tr>
            <th>Policy Type</th>
            <th>Date Implemented</th>
            <th>Date Expires</th>
            <th>Source</th>
            </tr>`
            for (var i = 0; i < currentpoliciesp.length; i++) {
                infohtml += `<tr><th>
            ${currentpoliciesp[i][2]} </th><th> 
            ${currentpoliciesp[i][3]} / ${currentpoliciesp[i][4]} </th><th> `
                if (currentpoliciesp[i][5] == '12' & currentpoliciesp[i][6] == '31')
                    infohtml += `None</th><th> `
                else
                    infohtml += `${currentpoliciesp[i][5]} / ${currentpoliciesp[i][6]} </th><th> `
                if (currentpoliciesp[i][7].includes('web.archive.org')) {
                    url = currentpoliciesp[i][7].split('web.archive.org')[1].split('/')
                    url.shift()
                    url.shift()
                    url.shift()
                    if (url[0].includes('http'))
                        url.shift()
                    url = 'http://' + url.join('/')
                    infohtml += `<a href='${url}' target="_blank" rel="noopener noreferrer" >Source</a><br><a href='${currentpoliciesp[i][7]}' target="_blank" rel="noopener noreferrer" >(Archive)</a> </th></tr>`

                }
                else
                    infohtml += `<a href='${currentpoliciesp[i][7]}' target="_blank" rel="noopener noreferrer" >Source</a> </th></tr>`
            }
        }
        else
            infohtml += '<h3 style="color:white">Partial Closures</h3>&nbsp;&nbsp;&nbsp;No Partial Closures at this date'

        infohtml += `</table><h3 class="CDB-infowindow-subtitle" style="color:white">Covid-19 Stats:</h3>
<div id='countrychart'></div><div id='countrychart2'></div><div id='attr' style="font-size:10px">Source: <a href='https://github.com/CSSEGISandData/COVID-19'>JHU CSSE COVID-19 Data</a></div><div id='heatmap'></div>
`
        document.getElementById('info').innerHTML = infohtml;
        if (document.getElementById('info').style.display == "none" | document.getElementById('info').style.display == "") {
            document.getElementById('info').style.display = 'block';
            document.getElementById('map').style.width = mapwidth - document.getElementById('info').offsetWidth + 'px'
        }//map.resize()

        var casesforchart = []
        var deathsforchart = []
        //console.warn(vars.iso3.value)

        chartwidth = document.getElementById('subinfo').offsetWidth * .9;

        if (getCountryByCode(iso3).length > 0) {
            casefromjson = getCountryByCode(iso3)[0].properties;

            for (var month = 1; month <= currentMonth + 1; month++) {
                for (var day = 1; day <= days[month - 1]; day++) {
                    if ((month == currentMonth + 1) & (day > currentday)) {
                        break;
                    }
                    if ((month == 1) & day < 22) {
                        continue;
                    }
                    casesforchart.push(casefromjson[String(month) + "_" + String(day) + "_20"]);
                    deathsforchart.push(casefromjson[String(month) + "_" + String(day) + "_20d"]);
                }
            }


            var trace2 = {
                type: "bar",
                mode: "lines",
                name: 'Deaths',
                x: datesforchart,
                y: deathsforchart,
                marker: { color: '#bf000d' },
                line: { color: '#7F7F7F' },
                yaxis: 'y'
            }

            var trace1 = {
                type: 'bar',
                x: datesforchart,
                y: casesforchart,
                name: 'Confirmed Cases',
                mode: 'lines',
                marker: { color: '#7F7F7F' },
                line: { color: '#9f9f9f' }
            }


            var data = [trace1, trace2];

            var layout = {
                width: chartwidth,
                height: chartwidth / 2,
                paper_bgcolor: '#222',
                plot_bgcolor: '#222',
                margin: {
                    l: 20,
                    r: 20,
                    b: 40,
                    t: 20,
                    pad: 4
                },
                showlegend: false,
                xaxis:
                {
                    autorange: true,
                    gridcolor: '#ffffff10',
                    tickfont: {
                        family: '"Poppins",Old Standard TT, serif',
                        color: '#ffffff80',
                        size: 14
                    },
                    tickcolor: '#ffffff80',
                    tickmode: "auto",
                    nticks: 8,
                    fixedrange: true,
                    tickformat: '%b'
                },
                yaxis:
                {

                    hoverformat: ".3s",
                    gridcolor: '#ffffff10',
                    tickfont: {
                        family: 'Poppins,Old Standard TT, serif',
                        color: '#ffffff80',
                        size: 14
                    },
                    tickcolor: '#ffffff80',
                    autorange: true,
                    fixedrange: true,
                    automargin: true
                },
                yaxis2: {
                    autorange: true,
                    automargin: true,
                    overlaying: 'y',
                    side: 'right'
                }
            };
            Plotly.newPlot('countrychart', data, layout, { displayModeBar: false })

        }
        else {
            document.getElementById('countrychart').innerHTML = "No Case Data Available"
        }

        var now = new Date();
        var start = new Date(now.getFullYear(), 0, 0);
        var dayone = start.getDay();
        var diff = (now - start) + ((start.getTimezoneOffset() - now.getTimezoneOffset()) * 60 * 1000);
        var oneDay = 1000 * 60 * 60 * 24;
        var daysofar = Math.floor(diff / oneDay);

        xvalues = []
        yvalues = []
        zvalues = []

        for (var day = dayone; day > 0; day--) {
            zvalues.push(null);
        }

        for (var day = 0; day <= daysofar; day++) {
            yvalues.push(Math.floor(day / 7))
            xvalues.push((day) % 7)
            //zvalues.push((day%8)/8)
        }

        categoriespriority = { "Workers Exception": 0, "Specific Country(ies) Exception": 1, "Citizen Exception": 2, "Essentials-only Exception": 3, "Visa ban": 4, "Citizenship ban": 5, "Travel history ban": 6, "Border Closure": 7, "NONE": 8 };

        for (var month = 1; month <= currentMonth + 1; month++) {
            for (var day = 1; day <= days[month - 1]; day++) {
                if ((month == currentMonth + 1) & (day > currentday)) {
                    break;
                }
                // if((month==1) & day< 22){
                //   continue;
                // }
                policy = 8
                for (var i = 0; i < currentcountry.length; i++) {
                    if (((month > currentcountry[i][3]) | ((month == currentcountry[i][3]) & (day >= currentcountry[i][4]))) &
                        ((month < currentcountry[i][5]) | ((month == currentcountry[i][5]) & (day <= currentcountry[i][6])))) {
                        if (policy > categoriespriority[currentcountry[i][2]]) {
                            policy = categoriespriority[currentcountry[i][2]]
                        }
                    }
                    //else
                        //policy = 8;
                }
                zvalues.push(policy);

            }
        }
        const colors = ['#a8dbd9', '#85c4c9', '#4f90a6', '#2a5674', '#672044', '#ad466c', '#e38191', '#ffc6c4', '#888']

        colorscaleValue = []
        for (var j = 0; j <= 8; j++) {
            colorscaleValue.push([j / 9, colors[j]])
            colorscaleValue.push([(j + 1) / 9, colors[j]])
        }

        var heatmapplot = document.getElementById('heatmap'),
            d3 = Plotly.d3,
            data = [{
                x: xvalues,
                y: yvalues,
                z: zvalues,
                zmin: 0,
                zmax: 8,
                type: 'heatmap',
                colorscale: colorscaleValue,
                showscale: false,
                xgap: 3,
                ygap: 3,
                hoverongaps: false,
                hoverinfo: 'none',
                colorbar: {
                    autotick: false,
                    tick0: 0,
                    dtick: 1,
                },
            }],
            layout = {
                width: 400,
                height: 880,
                paper_bgcolor: '#222',
                plot_bgcolor: '#222',
                annotations: [],
                xaxis: {
                    ticks: '',
                    side: 'top',
                    tickmode: "array",
                    ticktext: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    tickvals: [0, 1, 2, 3, 4, 5, 6],
                    showline: false,
                    showgrid: false,
                    zeroline: false,
                    fixedrange: true,
                    tickfont: {
                        family: 'Poppins,Old Standard TT, serif',
                        size: 14,
                        color: '#fff'
                    },
                },
                yaxis: {
                    ticks: '',
                    ticksuffix: ' ',
                    //    width: 700,
                    //  height: 700,
                    tickmode: "array",
                    ticktext: ["Jan ", "Feb ", "Mar ", "Apr ", "May ", "Jun ", "Jul ", "Aug ", "Sep ", "Oct ","Nov "],
                    tickvals: [0, 4, 8, 13, 17, 22, 26, 30, 35,39,43],
                    autorange: 'reversed',
                    autosize: true,
                    showline: false,
                    fixedrange: true,
                    showgrid: false,
                    zeroline: false,
                    tickfont: {
                        family: 'Poppins,Old Standard TT, serif',
                        size: 14,
                        color: '#fff'
                    },
                }
            };

        dayannotation = dayone
        for (var month = 1; month <= currentMonth + 1; month++) {
            for (var day = 1; day <= days[month - 1]; day++) {
                if ((month == currentMonth + 1) & (day > currentday)) {
                    break;
                }
                if ((zvalues[dayannotation] == 0) | (zvalues[dayannotation] == 7)) {
                    var textcolor = 'black';
                } else {
                    var textcolor = 'white';
                }

                var result = {
                    xref: 'x1',
                    yref: 'y1',
                    x: xvalues[dayannotation],
                    y: yvalues[dayannotation],
                    text: day,
                    //hovertext : monthdisplay[month-1] +"." + day,
                    font: {
                        family: 'Poppins,Arial',
                        size: 11,
                        color: textcolor
                    },
                    showarrow: false,
                }
                layout.annotations.push(result);

                dayannotation += 1
            }
        }


        /*for ( var i = 0; i < zvalues.length; i++ ) {
            var currentValue = zvalues[i];
            var result = {
              //x: xvalues[i],
              //y: yvalues[i],
              //text: zvalues[i],
              showarrow: false,
            };
            layout.annotations.push(result);
        }*/
        //{staticPlot: true}


        Plotly.newPlot('heatmap', data, layout, { displayModeBar: false });

        // heatmapplot.on('plotly_afterplot', function(){
        //     Plotly.d3.selectAll(".infolayer")
        //           .on("click", function(d) {
        //            console.warn(d3.select(this).text())
        //             alert("Hello, I am " + d);
        //           });
        // });


        //document.getElementById('toolbox').style.marginRight = '20%';
        //document.getElementById('toolbox').style.marginBottom = '0';
        heatmapplot.on('plotly_click', function (data) {
            if (data.points[0].pointIndex <= 23) {
                date = 0
            }
            else
                date = data.points[0].pointIndex - 23
            slider.set(data.points[0].pointIndex - 23)
            drawinfo(iso3, country, date)
        });

    }


    function dragElement(elmnt) {
        var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        elmnt.onmousedown = dragMouseDown;


        function dragMouseDown(e) {
            e = e || window.event;
            // get the mouse cursor position at startup:
            pos3 = e.clientX;
            pos4 = e.clientY;

            // store the current viewport and element dimensions when a drag starts
            rect = elmnt.getBoundingClientRect();
            viewport.bottom = window.innerHeight - PADDING;
            viewport.left = PADDING;
            viewport.right = window.innerWidth - PADDING;
            viewport.top = PADDING;

            document.onmouseup = closeDragElement;
            // call a function whenever the cursor moves:
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            // calculate the new cursor position:
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;

            // check to make sure the element will be within our viewport boundary
            var newLeft = elmnt.offsetLeft - pos1;
            var newTop = elmnt.offsetTop - pos2;

            if (newLeft < viewport.left
                || newTop < viewport.top
                || newLeft + rect.width > viewport.right + 350
                || newTop + rect.height > viewport.bottom
            ) {
                // the element will hit the boundary, do nothing...
            } else {
                // set the element's new position:
                elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
                elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
            }
        }

        function closeDragElement() {
            /* stop moving when mouse button is released:*/
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }

    function animatehandler() {
        if ((slider.get() < Object.keys(pipDisplay).length - 1) & (animate == 1)) {
            slider.set(parseInt(slider.get()) + 5)
            setTimeout(animatehandler, 200)
        }
        else {
            document.getElementById('animatecontrol').innerHTML = `<path style="fill:white" d="M8 5v14l11-7z"/>`
            animate = 0;
        }
    }

    function hideInfo() {
        displayInfo = 0;
        document.getElementById('info').style.display = 'none';
        document.getElementById('map').style.width = '100%';
        //document.getElementById('toolbox').style.marginRight = '0';

    }

    const maptransition = document.getElementById('map');
    maptransition.addEventListener('transitionend', function () {
        map.resize();
        mapwidth = document.getElementById('map').offsetWidth
        drawHistogram();
    });


    function readinfo(strData, strDelimiter) {
        // Check to see if the delimiter is defined. If not,
        // then default to comma.
        strDelimiter = (strDelimiter || ",");

        // Create a regular expression to parse the CSV values.
        var objPattern = new RegExp(
            (
                // Delimiters.
                "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +

                // Quoted fields.
                "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +

                // Standard fields.
                "([^\"\\" + strDelimiter + "\\r\\n]*))"
            ),
            "gi"
        );


        // Create an array to hold our data. Give the array
        // a default empty first row.
        var arrData = [[]];

        // Create an array to hold our individual pattern
        // matching groups.
        var arrMatches = null;


        // Keep looping over the regular expression matches
        // until we can no longer find a match.
        while (arrMatches = objPattern.exec(strData)) {

            // Get the delimiter that was found.
            var strMatchedDelimiter = arrMatches[1];

            // Check to see if the given delimiter has a length
            // (is not the start of string) and if it matches
            // field delimiter. If id does not, then we know
            // that this delimiter is a row delimiter.
            if (
                strMatchedDelimiter.length &&
                strMatchedDelimiter !== strDelimiter
            ) {

                // Since we have reached a new row of data,
                // add an empty row to our data array.
                arrData.push([]);

            }

            var strMatchedValue;

            // Now that we have our delimiter out of the way,
            // let's check to see which kind of value we
            // captured (quoted or unquoted).
            if (arrMatches[2]) {

                // We found a quoted value. When we capture
                // this value, unescape any double quotes.
                strMatchedValue = arrMatches[2].replace(
                    new RegExp("\"\"", "g"),
                    "\""
                );

            } else {

                // We found a non-quoted value.
                strMatchedValue = arrMatches[3];

            }


            // Now that we have our value string, let's add
            // it to the data array.
            arrData[arrData.length - 1].push(strMatchedValue);
        }

        // Return the parsed data.
        return (arrData);
    }

    function iOS() {
        return [
            'iPad Simulator',
            'iPhone Simulator',
            'iPod Simulator',
            'iPad',
            'iPhone',
            'iPod'
        ].includes(navigator.platform)
            // iPad on iOS 13 detection
            || (navigator.userAgent.includes("Mac") && "ontouchend" in document)
    }

}