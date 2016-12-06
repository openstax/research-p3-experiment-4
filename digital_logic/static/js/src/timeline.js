class Timeline {
  constructor(paramaters) {
    this.progress = {
      currentLocation: -1,
    }

  }
}

class TimelineItem {
  constructor(parameters) {
    this.progress = {
      currentRepetition: 0,
      currentIteration: 0,
      done: false,
    }
  }
}
