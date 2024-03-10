/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/2404589803/hf-daily-paper-newsletter-chinese/internal"
	"github.com/spf13/cobra"
)

var SubTitle string

// currentCmd represents the current command
var currentCmd = &cobra.Command{
	Use:   "current",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		// - how to get argument
		subtitle, _ := cmd.Flags().GetString("subtitle")

		config := internal.GetConfigs("../configs.yaml")
		general_config := config.General
		email_config := config.Email
		// article := internal.Article{}
		// 1. get YAML files in current directory
		filenames := internal.GetListOfFilesAt("../current", ".yaml")
		fmt.Println(filenames)
		// 2. open each files & parse them to Article
		articles := []internal.Article{}
		for _, filename := range filenames {
			buf, _ := ioutil.ReadFile(filename)
			articles = append(articles, internal.ParseArticle(string(buf)))
		}
		articleTuples := internal.ZipArticleTuples(articles, email_config.ContentLinkBtnTitle, email_config.BgColor)
		fmt.Println(articleTuples)

		tag_dest, _ := filepath.Abs("../tags")
		seqNum := internal.GetSequenceNumberFromDirs(tag_dest)
		// 3. fill out template
		email := internal.Email{
			Title:       fmt.Sprintf("%s #%d", email_config.Title, seqNum),
			FooterTitle: email_config.FooterTitle,
			Header: internal.Head{
				Title:                 email_config.HeaderTitle,
				Description:           email_config.HeaderDescription,
				ImageURL:              email_config.HeaderImageURL,
				CommunityLink:         email_config.CommunityLink,
				CommunityLinkBtnTitle: email_config.CommunityLinkBtnTitle,
				BgColor:               email_config.BgColor,
			},
			FirstSection: internal.Section{
				Title: email_config.SectionTitle,
			},
			ArticleTuples: articleTuples,
		}
		fmt.Println(email)

		f, err := os.Create("output.html")
		if err != nil {
			fmt.Println(err)
		}
		defer f.Close()

		// 4. send email
		sender_addr := os.Getenv("EMAIL")
		sender_pass := os.Getenv("PASSWORD")
		subject := email_config.Title + "(" + subtitle + ")"
		r := internal.NewRequest(sender_addr, sender_pass, config.Email.Receivers, subject)
		r.Send("../templates", email)

		// 5. archive
		base := fmt.Sprintf("%s/blob/%s/", general_config.GitHubRepoURL, general_config.GitBranch)
		archive_dest, _ := filepath.Abs("../archive")
		archive_destinations := internal.MoveFiles(filenames, archive_dest, base)

		for i, archive_destination := range archive_destinations {
			internal.RecordArticleByTags(articles[i], tag_dest, archive_destination)
		}
	},
}

func init() {
	publishCmd.AddCommand(currentCmd)
	currentCmd.Flags().StringVarP(&SubTitle, "subtitle", "s", "", "subtitle to be concatenated to the main title defined in configs.yaml")
}
