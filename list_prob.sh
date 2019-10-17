aws support describe-trusted-advisor-checks
	--region us-east-1
	--language en
	--output table
	--query "checks[*].name"