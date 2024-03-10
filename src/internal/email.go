package internal

import (
	"bytes"
	"text/template"
)

type Head struct {
	Title                 string
	Description           string
	ImageURL              string
	CommunityLink         string
	CommunityLinkBtnTitle string
	BgColor               string
}

type Section struct {
	Title string
}

type ArticleTuple struct {
	Article1  Article
	Article2  Article
	LinkTitle string
	BgColor   string
}

type Email struct {
	Title         string
	FooterTitle   string
	Header        Head
	FirstSection  Section
	ArticleTuples []ArticleTuple // has to be
}

type Request struct {
	from     string
	to       []string
	subject  string
	body     string
	password string
}

const (
	MIME = "MIME-version: 1.0;\nContent-Type: text/html; charset=\"UTF-8\";\n\n"
)

func add(x, y int) int {
	return x + y
}

func sub(x, y int) int {
	return x - y
}

func NewRequest(from string, password string, to []string, subject string) *Request {
	return &Request{
		from:     from,
		to:       to,
		subject:  subject,
		password: password,
	}
}

func (r *Request) parseTemplate(templatePath string, data interface{}) error {
	templateFilenames := GetTemplatesInDir(templatePath)
	tmpl := template.New("huggingface_template").Funcs(template.FuncMap{
		"add": add,
		"sub": sub,
	})
	var err error
	tmpl, err = tmpl.ParseFiles(templateFilenames...)
	if err != nil {
		return err
	}

	buffer := new(bytes.Buffer)
	if err = tmpl.ExecuteTemplate(buffer, "hf_newsletter_template.gohtml", data); err != nil {
		return err
	}
	r.body = buffer.String()
	return nil
}
