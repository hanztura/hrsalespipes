Vue.component('animated-number', AnimatedNumber)

const DashboardValueCard = {
  props: ['value', 'text'],
  template: `
    <v-col cols="12" md=4>
      <v-card
        class="mx-auto text-center"
        outlined
        elevation=1>
        <v-card-text>
          <p class="font-weight-black headline">
            <animated-number
              class="display-1"
              :value="value"
              :duration="2000"
              :round="0"/>
          </p>
          <p class="title mb-0">[[ text ]]</p>
        </v-card-text>
      </v-card>
    </v-col>
  `,
}
const DashboardValueCard2 = {
  name: 'DashCard',
  props: ['value', 'text', 'icon', 'url'],
  template: `
    <v-col cols="12" md=4>
      <v-card
        class="mx-auto"
        outlined>
        <v-list-item three-line>
          <v-list-item-avatar>
            <v-icon large>[[ icon ]]</v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title class="headline mb-1 primary--text">
            <animated-number
              class="display-1"
              :value="value"
              :duration="2000"
              :round="0"/>
            </v-list-item-title>
            <v-list-item-subtitle><a :href="url">[[ text ]]</a></v-list-item-subtitle>
          </v-list-item-content>

        </v-list-item>
      </v-card>
    </v-col>
  `
}

Vue.component('graph-card', {
  name: 'GraphCard',
  props: [
    'chartData',
    'defaultChartType',
    'chartTypes',
    'title',
    'href',
  ],
  data: () => {
    return {
      chartType: 'ColumnChart',
      options: {
        legend: {
          position: 'bottom'
        }
      }
    }
  },

  computed: {
    hasData: function() {
      return this.chartData.length > 1
    }
  },

  mounted() {
    this.chartType = this.defaultChartType;
  },

  template: `
    <v-card
      class="mx-auto text-center"
      color="primary"
      outlined
      dark
      elevation=1>
      <v-card-text>
        <div class="title font-weight-thin"><a class="white--text" :href="href">[[ title ]]</a></div>
      </v-card-text>

      <template v-if="hasData">
        <v-card-text>
          <v-sheet>
            <g-chart
              :type="chartType"
              :data="chartData"
              :options="options"
            />
          </v-sheet>
        </v-card-text>

        <v-card-actions>
          <v-row align="center" justify="center">
            <v-btn
              class="mx-2"
              v-for="ct in chartTypes"
              :key="ct.type"
              :title="ct.text"
              @click="changeChartType(ct.type, ct.options)">
              <v-icon>[[ ct.icon ]]</v-icon>
            </v-btn>
          </v-row>
        </v-card-actions>
      </template>

      <v-card-text v-else>
        <v-sheet color="rgba(0, 0, 0, .12)">
          <p>No data available.</p>
        </v-sheet>
      </v-card-text>
    </v-card>
  `,
  methods: {
    changeChartType: function(value, options={}) {
      this.chartType = value;
      if (options) { this.options = options; }
    },
  }
})

new Vue({
  name: 'DashboardApp',
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [],
    chartTypes: [
      {
        'type': 'ColumnChart',
        'text': 'Column',
        'options': {
          legend: {
            position: 'bottom'
          }
        },
        'icon': 'mdi-chart-bar',
      },
      {
        'type': 'BarChart',
        'text': 'Bar',
        'options': {
          legend: {
            position: 'bottom'
          }
        },
        'icon': 'mdi-chart-bar rotate-90',
      },
      {
        'type': 'PieChart',
        'text': 'Pie',
        'options': {
          legend: {
            position: 'bottom'
          }
        },
        'icon': 'mdi-chart-pie',
      },
      {
        'type': 'LineChart',
        'options': {
          legend: {
            position: 'bottom'
          }
        },
        'text': 'Line',
        'icon': 'mdi-chart-line',
      },
    ],
    dashboardItemsNumber: [],
    sjatpi: data.sjatpi,
    sjpc: data.sjpc,
    tnfipc: data.tnfipc,
    tnfipcp12m: data.tnfipcp12m,
    ytdcp: [],
    transformTheseData: [
      {
        sourceId: 'dataSuccessfulJobsAllTimePerIndustry',
        dataField: 'sjatpi',
        titleField: 'job_candidate__job__client__industry',
      },
      {
        sourceId: 'dataSuccessfulJobsPerConsutant',
        dataField: 'sjpc',
        titleField: 'job_candidate__consultant__name',
      },
      {
        sourceId: 'dataTNFIPerConsultant',
        dataField: 'tnfipc',
        titleField: 'job_candidate__consultant__name',
      },
      {
        sourceId: 'dataTNFIPerConsultantLast12Months',
        dataField: 'tnfipcp12m',
        titleField: 'job_candidate__consultant__name',
      },
    ],
  }),

  computed: {
    graphItems: function() {
      return [
        this.ytdcpData,
        this.tnfipc,
        this.tnfipcp12m,
        this.sjatpi,
        this.sjpc,
      ]
    },
    ytdcpDataBySources: function(){
      // get sources
      let sources = _.groupBy(this.ytdcp.value, 'cvSource');
      return sources;
    },
    ytdcpDataByClientId: function(){
      let clients = _.groupBy(this.ytdcp.value, 'id');
      return clients
    },
    transformedYTDCP: function(){
      ytdcp = [
        ['Client', 'Total'],
      ]
      let sources = _.keys(this.ytdcpDataBySources);

      _.forEach(sources, (source, index) => {
        ytdcp[0].push(source) - 1;
      });

      _.forEach(this.ytdcpDataByClientId, (rows, clientId)=>{
        let data = new Array(sources.length + 2);
        let total = 0;

        _.forEach(rows, (row, index) => {
          let source = row.cvSource;
          let sourceIndex = ytdcp[0].indexOf(source);

          // set client name
          if (index == 0) { data[0] = row.client }
          data[sourceIndex] = row.value;
          total += row.value;
        });

        data[1] = total;
        ytdcp.push(data);
      });
      return ytdcp;
    },
    ytdcpData: function() {
      let data = {
        title: this.ytdcp.title,
        data: this.transformedYTDCP,
        href: this.ytdcp.url
      }
      return data;
    }
  },

  methods: {
    changeChartType: function(property, value) {
      this.$set(this, property, value);
    },
    transformGraphData: function(sourceId, dataField, titleField) {
      let data = document.getElementById(sourceId).value;
      data = JSON.parse(data);

      // set value label
      this.$set(this[dataField][0], 1, data.title);
      // this.sjpc[0][1] = data.title;

      // transform data to be consumed by a graph
      let title = data.title;
      let href = data.url;
      data = _.map(data.value, (graph) => {
        // graph is the value attribute from django
        let value = graph.value ? graph.value : [];
        return [
          graph[titleField],
          value
        ]
      });
      data = this[dataField].concat(data);
      data = {
        data: data,
        title: title,
        href: href
      }

      this.$set(this, dataField, data);
    },
    setGraphData: function() {
      let _this = this;

      _.forEach(this.transformTheseData, (data) => {
        _this.transformGraphData(data.sourceId, data.dataField, data.titleField);
      });
    }
  },

  beforeMount(){
    this.setGraphData();
  },

  mounted() {
    this.updateBreadcrumbs();
    this.setDataChoices('dataDashboardItemsNumber', 'dashboardItemsNumber');
    this.setDataChoices('dataYTDClientPerformance', 'ytdcp');
  },

  components: {
    'dashboard-value-card': DashboardValueCard,
    'dash-card': DashboardValueCard2
  }

});