<template>
  <div>
    <div class="grid">
      <div class="col-2">
        <Dropdown showClear v-model="selectedcustomerType" :options="customer_types" optionLabel="name"
          placeholder="Select a customer type" class="w-full" />
      </div>
      <div class="col-2">
        <Dropdown showClear :options="provinces"  v-model="selectedProvince" @change="selectedProvicneChanged" optionLabel="name"
        placeholder="Select a Province" class="w-full" />
      </div>
      <div class="col-2">
        <Dropdown showClear :options="districts"  v-model="selectedDistrict" optionLabel="name"
        placeholder="Select a District" class="w-full" />
      </div>
      <div class="col-2">
        <span class="p-float-label">
          <AutoComplete v-model="selectedCustomer" inputId="ac" optionLabel="customer_name" :suggestions="customers" @complete="search" />
          <label for="ac">Customer</label>
        </span>
        
      </div>
      <div class="col-1">
        <Button label="Filter" icon="pi pi-search" @click="onFilterClick"/>
      </div>
      <div class="col-2 text-center title">
        {{ moment(start).format('DD MMM') }} , {{ moment(end).subtract(1, 'days').format('DD MMM') }} 
        {{ moment(end).subtract(1, 'days').format('YYYY') }}

      </div>
      <div class="col-1">
        <div class="flex justify-content-end">

          <Button @click="onPrevNext('prev')" icon="pi pi-angle-double-left"
            class="border-noround-right border-y-none border-left-none" style="height: 32px;"></Button>
          <Button @click="todayClick" class="border-noround border-none" style="height: 32px;"><img class="icon-set-svg"
              :src="iconTodayCalendar" /></Button>
          <Button @click="onPrevNext('next')" class="border-noround-left border-y-none border-right-none"
            style="height: 32px;" icon="pi pi-angle-double-right"></Button>
        </div>
      </div>
    </div>
    <div class="body">
      <FullCalendar ref="fullCalendar" :options="calendarOptions">
        <template v-slot:eventContent="{ event }">
          
          <div style="cursor: pointer;">
            <div class="flex">
              <div class="geust-title">
                {{ event.title }} ({{ moment(event.start).format('DD-MMM') }}, {{ moment(event.end).format('DD-MMM') }}), Last Order {{ event.last_month_order }}, {{event.current_order}}
           
              </div>
            </div>
          </div>
        </template>
      </FullCalendar>
    </div>
  </div>
</template>

<script setup type="module">
// import '@fullcalendar/core/vdom'
import iconTodayCalendar from '@/assets/svg/calendar-today-icon.svg'

import FullCalendar from '@fullcalendar/vue3'
import interactionPlugin from '@fullcalendar/interaction'
import resourceTimelinePlugin from '@fullcalendar/resource-timeline';
import { ref, reactive, onMounted } from 'vue'
import { FrappeApp } from 'frappe-js-sdk'
import moment from 'moment'


let selectedProvince = ref();
let selectedcustomerType = ref();
let selectedCustomer = ref();
let selectedDistrict = ref();
let selectedProvicne = ref();
let provinces = ref([]);
let customer_types = ref([]);
let customers = ref([]);
let districts = ref([]);
let start = ref()
let end = ref();
const fullCalendar = ref(null)
onMounted(() => {
  const frappe = new FrappeApp()
  const db = frappe.db()
  db.getDocList('Province').then((r) => {
    provinces.value = r
  })
  db.getDocList('Customer Type').then((r) => {
    customer_types.value = r
  })
 
  db.getDocList('Province',{fields:['name']}).then((r) => {
    provinces.value = r
  })
})

function selectedProvicneChanged(event){
  const frappe = new FrappeApp()
  const db = frappe.db()
  db.getDocList('District',{fields:['name'],filters: [['province', '=',  event.value.name ]]}).then((r) => {
    districts.value = r
  })
}

function resourceColumn() {
  return [
    {
      labelText: 'Customer',
      headerContent: 'Customer'
    },
    {
      field: 'province',
      headerContent: 'Province',
    },
    {
      field: 'customer_type',
      headerContent: 'Type',
    },
  ]

}
function onInitialDate() {
  localStorage.setItem('start_date', moment().subtract(3, 'days').format('YYYY-MM-DD'))
  localStorage.setItem('end_date', moment().add(1, 'months').subtract(1, 'days').format('YYYY-MM-DD'))
  return {
    start: moment().subtract(3, 'days').format('YYYY-MM-DD'),
    end: moment().add(1, 'months').subtract(1, 'days').format('YYYY-MM-DD')
  }

}

const initialDate = onInitialDate()
let fullcalendarInitialDate = ref(initialDate.start)
const calendarOptions = reactive({
  plugins: [interactionPlugin, resourceTimelinePlugin],
  initialView: 'resourceTimeline',
  schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
  stickyHeaderDates: true,
  timeZone: 'UTC',
  selectable: true,
  refetchResourcesOnNavigate: true,
  eventResizableFromStart: true,
  refetchResourcesOnNavigate: true,
  nowIndicator: true,
  resourceAreaWidth: "400px",
  headerToolbar: false,
  initialDate: fullcalendarInitialDate.value,
  dateIncrement: { days: 3 },
  height: 'auto',
  resourceAreaColumns: resourceColumn(),
  slotLabelDidMount: function (info) {
    const d = moment(info.date).format("DD")
    const day = moment(info.date).format("ddd")
    const current_date = moment().format("yyyy-MM-DD")
    if (moment(info.date).format("yyyy-MM-DD") == current_date) {
      info.el.getElementsByTagName("a")[0].innerHTML = "<div class='current_day line-height-15 border-round-lg px-3 py-2' style='font-size: 12px;'><span class='font-light'>" + day + "</span><br/>" + d + "<br/><span class='font-light'>" + moment(info.date).format("MMM") + "</span></div>"
    } else {
      if (day == "Sat" || day == "Sun") {
        info.el.getElementsByTagName("a")[0].innerHTML = "<div class='line-height-15  border-round-lg px-3 py-2' style='color:red;font-size: 12px;'><span class='font-light'>" + day + "</span><br/>" + d + "<br/><span class='font-light'>" + moment(info.date).format("MMM") + "</span></div>"
      }
      else {
        info.el.getElementsByTagName("a")[0].innerHTML = "<div class='line-height-15  border-round-lg px-3 py-2' style='font-size: 12px;'><span class='font-light'>" + day + "</span><br/>" + d + "<br/><span class='font-light'>" + moment(info.date).format("MMM") + "</span></div>"
      }
    }
  },

  visibleRange: function (currentDate) {
    const startDate = initialDate.start
    const endDate = initialDate.end
    return { start: startDate, end: endDate };
  },
  resourceLabelDidMount: function (info) {

  },
  slotLabelFormat: function (date) {

    return date
  },
  eventClick: ((info) => {
    const data = info.event._def.extendedProps;
    window.open(window.location.origin + "/app/quotation/" + info.event._def.publicId, "_blank")
  }),
  select: (($event) => {
    let param = {
      start: $event.startStr,
      end: $event.endStr,
      customer: $event.resource._resource.id
    }
    localStorage.setItem('quotation-param', JSON.stringify(param))
    window.open(window.location.origin + "/app/quotation/new-quotation-1", "_blank")
  }),
  resources: function (info, successCallback, failureCallback) {
    const frappe = new FrappeApp()
    const call = frappe.call()
    call.get('truck_delivery.truck_delivery.doctype.customer.customer.get_resourses',{
      district:selectedDistrict.value?.name,
      customer:selectedCustomer.value?.name,
    }).then((r) => {
      successCallback(r.message)
    })
  },

  events: function (info, successCallback, failureCallback) {
    const frappe = new FrappeApp()
    const call = frappe.call()
    start = moment(info.start).format('yyyy-MM-DD')
    end = moment(info.end).format('yyyy-MM-DD')
    call.get('truck_delivery.truck_delivery.doctype.quotation.quotation.get_customer_quotations', {
      start: start,
      end: end,
      // province:selectedProvince.value?.name,
      customer_type:selectedcustomerType.value?.name,
      customer:selectedCustomer.value?.name,
    }).then((r) => {
      successCallback(r.message)
    })
  }
})
function onProvinceChanage(a){
  db.getDocList('District',{fields:['name'],filters: [['prorince', '=', selectedProvince.value.name]]}).then((r) => {
    districts.value = r
  })
}
const search = (event) => {
  const frappe = new FrappeApp()
  const db = frappe.db()
  db.getDocList('Customer',{fields: ['name', 'customer_name'],filters: [['customer_name', 'Like', '%'+ event.query +'%']]}).then((r) => {
    customers.value = r
  })
}
function onFilterClick(){
  const cal = fullCalendar.value.getApi()
  cal.refetchEvents()
  cal.refetchResources()
}
function todayClick(){
    const cal = fullCalendar.value.getApi()
    const startDate = initialDate.start
    const endDate = initialDate.end
    cal.changeView('resourceTimeline', { start: moment(startDate).format('YYYY-MM-DD'), end: moment(endDate).format('YYYY-MM-DD') });
    localStorage.setItem('start_date', moment(startDate).format('YYYY-MM-DD'))
    localStorage.setItem('end_date', moment(endDate).format('YYYY-MM-DD'))
    cal.refetchEvents()
  cal.refetchResources()
  }
function onPrevNext(key) {
  const cal = fullCalendar.value.getApi()
  if (key == 'prev') {
    const currenct_start = localStorage.getItem('start_date')
    const current_end = localStorage.getItem('end_date')
    cal.changeView('resourceTimeline', { start: moment(currenct_start).subtract(3, 'days').format('YYYY-MM-DD'), end: moment(current_end).add(3, 'days').format('YYYY-MM-DD') });
    localStorage.setItem('start_date', moment(currenct_start).subtract(3, 'days').format('YYYY-MM-DD'))
    localStorage.setItem('end_date', moment(current_end).subtract(3, 'days').format('YYYY-MM-DD'))
    cal.refetchEvents()
  cal.refetchResources()
  } else {
    const currenct_start = localStorage.getItem('start_date')
    const current_end = localStorage.getItem('end_date')
    cal.changeView('resourceTimeline', { start: moment(currenct_start).add(3, 'days').format('YYYY-MM-DD'), end: moment(current_end).add(3, 'days').format('YYYY-MM-DD') });
    localStorage.setItem('start_date', moment(currenct_start).add(3, 'days').format('YYYY-MM-DD'))
    localStorage.setItem('end_date', moment(current_end).add(3, 'days').format('YYYY-MM-DD'))
    cal.refetchEvents()
  cal.refetchResources()
  }
}

</script>
<style>
.body {
  font-family: 'Poppins','kh system' !important;
  height: calc(100vh - 65px);
  overflow-y: auto;
}

.fc-h-event {
  display: block;
  border-radius: 20px;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #4b4953;
}

.icon-set-svg {
  height: 16px;
}
.fc table{
  font-size: 13px!important; 
}
.fc-timeline-event:not(.fc-event-end)::after, .fc-timeline-event:not(.fc-event-start)::before{
  display: none!important;;
}
</style>