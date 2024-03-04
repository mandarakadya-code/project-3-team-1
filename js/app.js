// This function is called when the UI is initialized
// The chart that is loaded during initialization is a bar chart of the total emissions by year 
function init(){
    d3.json("http://127.0.0.1:5000/api/v1.0/annualEmissions").then(function(data) {
        let emission1970 = 0;
        let emission1980 = 0;
        let emission1990 = 0;
        let emission2000 = 0;
        let emission2010 = 0;
        let emission2022 = 0;
        for(em of data){
            if(em.year == 1970){
                emission1970 = emission1970+em.emission;
            }else if(em.year == 1980){
                emission1980 = emission1980+em.emission;
            }else if(em.year == 1990){
                emission1990 = emission1990+em.emission;
            }else if(em.year == 2000){
                emission2000 = emission2000+em.emission;
            }else if(em.year == 2010){
                emission2010 = emission2010+em.emission;
            }else if(em.year == 2022){
                emission2022 = emission2022+em.emission;
            }
                // console.log(em);
        }
        // To display the percentage of chage year over year, we do the calculations in textValue
        let xValue = [1970, 1980, 1990, 2000, 2010, 2022];
        let yValue = [emission1970, emission1980, emission1990, emission2000, emission2010, emission2022];
        let totalEmissions = emission1970+emission1980+emission1990+emission2000+emission2010+emission2022;
        let textValue = [((emission1970/totalEmissions)*100).toFixed(2)+"%", ((emission1980/totalEmissions)*100).toFixed(2)+"%", 
            ((emission1990/totalEmissions)*100).toFixed(2)+"%", ((emission2000/totalEmissions)*100).toFixed(2)+"%", 
            ((emission2010/totalEmissions)*100).toFixed(2)+"%", ((emission2022/totalEmissions)*100).toFixed(2)+"%"]

        var dataPlot = [{
            x: xValue,
            y: yValue,
            text: textValue,
            textposition: 'auto',
            type: "bar"
            // transforms: [{
            //   type: 'sort',
            //   target: 'x',
            //   order: 'ascending'
            // }],
            // orientation: 'h'
          }];
          Plotly.newPlot('total-emissions', dataPlot);
});
}

// When the drop down value changes, we call the updatePlotly function
d3.selectAll("#selPeriod").on("change", updatePlotly);

function updatePlotly() {
    let dropdownMenu = d3.select("#selPeriod");
    let periodOfEmission = dropdownMenu.property("value");
    let emissionDataList = [];
    
    
    console.log(periodOfEmission);
    if(periodOfEmission == "currentEmission" || periodOfEmission == "historyEmission"){
        d3.json("http://127.0.0.1:5000/api/v1.0/annualEmissions").then(function(data) {
        
            let countryArray = data.map(function(country){
                return country.country;
            });
            var uniqueCtr = [...new Set(countryArray)];
            console.log("country array",uniqueCtr);
            let filterDataYear = [];
            let filterData;
            for(ctr of uniqueCtr){
                let emissionData = {
                    country:[],
                    year:[],
                    emission:[]
                };
                if(periodOfEmission == "currentEmission"){
                    filterData = data.filter(function(emData){
                        return emData.country == ctr && emData.year > 2009
                    });
                    filterDataYear.push(data.filter(function(emData){
                        return emData.country == ctr && emData.year == 2022 && (/^[A-Z]{3}$/).test(emData.code)
                    })[0]);
                }else if(periodOfEmission == "historyEmission"){
                    filterData = data.filter(function(emData){
                        return emData.country == ctr && emData.year >= 1960 && emData.year <= 1980
                    });
                    filterDataYear.push(data.filter(function(emData){
                        return emData.country == ctr && emData.year == 1979 && (/^[A-Z]{3}$/).test(emData.code)
                    })[0]);
                }
                
                let sortFilterData = filterData.sort((a,b) => b.year - a.year)
                emissionData.country.push(ctr);
                emissionData.year.push(sortFilterData.map(function(emDataFltr){
                    return emDataFltr.year;
                }));
                emissionData.emission.push(sortFilterData.map(function(emDataFltr){
                    return emDataFltr.emission;
                }));
                // console.log("emission data country",emissionData.country);
                emissionDataList.push(emissionData);
            }
            // console.log("Emission List",emissionDataList);
        let sortedByEmissionYear = filterDataYear.sort((a, b) => b.emission - a.emission);

        let slicedData = sortedByEmissionYear.slice(0, 10);
        
        
        var lineData = [];    
        for(country of slicedData.map(object => object.country)){
            let dataForLine = emissionDataList.filter(obj => {return obj.country == country})[0];
            
            var trace = {
                x: dataForLine.year[0],
                y: dataForLine.emission[0],
                mode: "lines+markers",
                name: country
            }
            lineData.push(trace);
        }
        Plotly.newPlot("line",lineData);

        var dataPlot = [{
            x: slicedData.map(object => object.country),
            y: slicedData.map(object => object.emission),
            type: "bar"
          }];
          Plotly.newPlot('barPeriod', dataPlot);
          
          console.log(filterDataYear);
          let slicedDataMap;
          if(periodOfEmission == "currentEmission"){
            slicedDataMap = sortedByEmissionYear.slice(0, 212);
          }else {
            slicedDataMap = sortedByEmissionYear.slice(0, 201);
          }
          console.log(slicedDataMap.map(object => object.country));

          var mapData = [{
            type: 'choropleth',
            locationmode: 'country names',
            locations: slicedDataMap.map(object => object.country),
            z: slicedDataMap.map(object => object.emission),
            text: slicedDataMap.map(object => object.country),
            colorscale: 'YlOrRd',
            // [
            //     [0,'rgb(5, 10, 172)'],[0.35,'rgb(40, 60, 190)'],
            //     [0.5,'rgb(70, 100, 245)'], [0.6,'rgb(90, 120, 245)'],
            //     [0.7,'rgb(106, 137, 247)'],[1,'rgb(220, 220, 220)']],
            autocolorscale: false,
            reversescale: true,
            marker: {
                line: {
                    color: 'rgb(180,180,180)',
                    width: 0.5
                }
            },
            tick0: 0,
            zmin: 10000,
            dtick: 1000000,
            colorbar: {
                autotic: false,
                // tickprefix: '$',
                title: 'CO2 emissions'
            }
      }];

      var layout = {
          title: 'CO2 Emissions by Countries',
          width: 1000,
          height: 800,
          geo:{
              showframe: false,
              showcoastlines: false,
              projection:{
                  type: 'mercator'
              }
          }
      };
      Plotly.newPlot("map", mapData, layout);
    
    });
    } else if(periodOfEmission == "emissionPerPerson"){
        d3.json("http://127.0.0.1:5000/api/v1.0/emissionsPerPerson").then(function(data) {
            let countryArray = data.map(function(country){
                return country.country;
            });
            var uniqueCtr = [...new Set(countryArray)];
            let filterDataYear = [];
            for(ctr of uniqueCtr){
                let emissionData = {
                    country:[],
                    year:[],
                    emission:[]
                };
                let filterData = data.filter(function(emData){
                    return emData.country == ctr && emData.year > 2009
                });
                filterDataYear.push(data.filter(function(emData){
                    return emData.country == ctr && emData.year == 2022 && (/^[A-Z]{3}$/).test(emData.code)
                })[0]);
                let sortFilterData = filterData.sort((a,b) => b.year - a.year)
                emissionData.country.push(ctr);
                emissionData.year.push(sortFilterData.map(function(emDataFltr){
                    return emDataFltr.year;
                }));
                emissionData.emission.push(sortFilterData.map(function(emDataFltr){
                    return emDataFltr.emission;
                }));
                // console.log("emission data country",emissionData.country);
                emissionDataList.push(emissionData);
            }
            let sortedByEmissionYear = filterDataYear.sort((a, b) => b.emission - a.emission);

        let slicedData = sortedByEmissionYear.slice(0, 10);
        
        var lineData = [];    
        for(country of slicedData.map(object => object.country)){
            let dataForLine = emissionDataList.filter(obj => {return obj.country == country})[0];
            
            var trace = {
                x: dataForLine.year[0],
                y: dataForLine.emission[0],
                mode: "lines+markers",
                name: country
            }
            lineData.push(trace);
        }
        Plotly.newPlot("line",lineData);

        var dataPlot = [{
            x: slicedData.map(object => object.country),
            y: slicedData.map(object => object.emission),
            type: "bar"
          }];
          Plotly.newPlot('barPeriod', dataPlot);

          let slicedDataMap = sortedByEmissionYear.slice(0, 212);
          console.log(slicedDataMap.map(object => object.country));

          var mapData = [{
            type: 'choropleth',
            locationmode: 'country names',
            locations: slicedDataMap.map(object => object.country),
            z: slicedDataMap.map(object => object.emission),
            text: slicedDataMap.map(object => object.country),
            colorscale: 'YlOrRd',
            // [
            //     [0,'rgb(5, 10, 172)'],[0.35,'rgb(40, 60, 190)'],
            //     [0.5,'rgb(70, 100, 245)'], [0.6,'rgb(90, 120, 245)'],
            //     [0.7,'rgb(106, 137, 247)'],[1,'rgb(220, 220, 220)']],
            autocolorscale: false,
            reversescale: true,
            marker: {
                line: {
                    color: 'rgb(180,180,180)',
                    width: 0.5
                }
            },
            tick0: 0,
            zmin: 10000,
            dtick: 1000000,
            colorbar: {
                autotic: false,
                // tickprefix: '$',
                title: 'CO2 emissions'
            }
      }];

      var layout = {
          title: 'CO2 Emissions by Countries',
          width: 1000,
          height: 800,
          geo:{
              showframe: false,
              showcoastlines: false,
              projection:{
                  type: 'mercator'
              }
          }
      };
      Plotly.newPlot("map", mapData, layout);
        });

        
    }
}

init();