class TotalsController extends window.StimulusModule.Controller {
  static targets = ["total"];

  added() {
    console.log(this.totalTargets)
    console.log("Added item")
  }

  removed() {
    console.log(this.totalTargets)
    console.log("Removed item")
  }
}

window.wagtail.app.register("totals-controller", TotalsController);
