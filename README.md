# B2B SaaS Product Launch Playbook

A go-to-market playbook for product marketing teams launching B2B SaaS products, from market research to the 90-day review.

**Live site:** https://archanacontent.github.io/b2b-saas/

Every B2B SaaS launch needs product marketing, sales, demand generation, product and leadership to move on the same date. Few start from a single plan. Each team works from its own idea of the buyer and the message, so launch day brings a website that promises one outcome and a sales deck that promises another. Buyers notice the gap before the team does.

The playbook replaces those separate plans with one product marketing process, from proving demand to measuring adoption. Its nine modules follow the order a launch runs in, and each one includes blank templates, a filled example and the mistakes that cost teams the most. Start at the first module for a new launch, or open the one your team needs this quarter.

## Modules

| # | Module | What it covers |
| :---: | :--- | :--- |
| 1 | [Market Research](docs/market-research.md) | Prove the problem and the demand before you spend. |
| 2 | [ICP And Personas](docs/icp-and-personas.md) | Define the companies to pursue and the people who decide. |
| 3 | [Competitive Intelligence](docs/competitive-intelligence.md) | Track rivals and give reps answers they can use mid-call. |
| 4 | [Positioning And Messaging](docs/positioning-and-messaging.md) | Settle one reason to buy and say it the same way everywhere. |
| 5 | [Go-To-Market Plan](docs/go-to-market-and-launch-plan.md) | Size the launch and fix who delivers what, and when. |
| 6 | [Launch Content](docs/launch-content-kit.md) | Build every asset from one message hierarchy. |
| 7 | [Sales Enablement](docs/sales-enablement.md) | Prepare reps to sell from the first day. |
| 8 | [Demand Generation](docs/demand-generation-support.md) | Keep every campaign tied to the positioning. |
| 9 | [Performance](docs/performance-and-optimisation.md) | Agree on success early and feed the results back. |

## Downloads

- **Word templates** - One file per module in [`templates/`](templates/).
- **Excel workbook** - [`launch-playbook-workbook.xlsx`](templates/launch-playbook-workbook.xlsx), with the opportunity scorecard, competitor tracker, RACI, timeline, channel plan, campaign brief, KPI framework and launch scorecard.
- **Sample sales deck** - [PowerPoint](templates/sample-sales-deck.pptx) and [PDF](templates/sample-sales-deck.pdf), built from Module 7.

The company in the worked examples is fictional. Market data is real and linked to its source.

## Build

```
pip install markdown python-docx openpyxl
python build/make_templates.py
python build/build.py
```

The site is written to `_site/`. Fonts are Literata and Public Sans, both under the SIL Open Font License.

## License

Licensed under [CC BY 4.0](LICENSE). Created by [Archana Panda](https://archanacontent.github.io/).
